import logging
from typing import Optional
import queue
import threading
import sys
from bot.lib.statusdb import Addstatus

from conversation.models import Treedj, Tweetdj
from conversation.models import create_leaf, create_tree
from community.helpers import get_community_twitter_tweepy_api
from community.models import Community
from bot.addstatusdj import addstatus

logger = logging.getLogger(__name__)

class ReplyCrawler(object):
    max_count = 100
    
    def __init__(self, community, root_id):
        self.community = community
        self.api = get_community_twitter_tweepy_api(
            self.community,
            backend=False
        )
        self.root_id = root_id
        self.q = queue.PriorityQueue(maxsize=0)
        self.since_id = root_id
        self.tree_init = ReplyCrawler.root_descendants(
            root_id,
            include_self=True
        )

    @staticmethod
    def root_descendants(root_id, include_self: bool = True):
        """Return list of descendants' ids
        """
        try:
            root = Treedj.objects.get(statusid=root_id)
        except Treedj.DoesNotExist:
            root = create_tree(root_id)
        if root:
            return sorted( 
                list(
                    root.get_descendants(include_self=include_self)
                    .values_list("statusid", flat=True)
                )
            )

    def get_screen_name(self, status_id):
        try:
            status = Tweetdj.objects.get(statusid=status_id)
            return status.json["user"]["screen_name"]
        except Tweetdj.DoesNotExist:
            logger.debug(f"Tweet {status_id} is not present in database.")
            addstatus(status_id, self.community.account.username)
            if Tweetdj.objects.filter(statusid=status_id).exists():
                return self.get_screen_name(status_id)
        except TypeError:
            if status.json is None:
                logger.debug(f"Tweet {status_id} json field is null.")
            return
        except KeyError:
            logger.debug(f"Tweet {status_id} json is buggy.")
            return

    def get_replies(self, status_id, since_id=None):
        screen_name = self.get_screen_name(status_id)
        if not since_id:
            since_id = status_id
        replies = self.search_reply_to(
            screen_name,
            community=self.community,
            since_id = since_id
        )
        logger.debug(f"{[(r.id, r.text) for r in replies]}")
        if len(replies) == ReplyCrawler.max_count:
            while True:
                hi = 0
                for x in (reply['id'] for reply in replies):
                    hi = max(x,hi)
                more_replies = self.search_reply_to(
                    screen_name,
                    community=self.community,
                    since_id = hi
                )
                if more_replies:
                    replies.extend(more_replies)
                if len(more_replies) < 100:
                    break
                replies = more_replies
        return replies

    def add_leaves(self, root_id):
        try:
            root = Treedj.objects.get(statusid=root_id)
        except Treedj.DoesNotExist:
            return
        replies = self.get_replies(root_id, since_id=root_id)
        if not replies:
            return
        root_descendants = ReplyCrawler.root_descendants(
            root.statusid,
            include_self=True
        )
        logger.debug(f"{root_descendants=}")
        # sort replies by id, by chronological order
        replies.sort(key = lambda i: i.id)
        for r in replies:
            if r.in_reply_to_status_id in root_descendants:
                create_leaf(r.id, r.in_reply_to_status_id)
        return root

    def build_tree(self, root_id):
        root = self.add_leaves(root_id)
        if not root:
            return
        root_descendants = ReplyCrawler.root_descendants(
            root.statusid,
            include_self=True
        )
        for r in root_descendants:
            self.add_leaves(r)
        tree_current = ReplyCrawler.root_descendants(
            root_id,
            include_self=True
        )
        new_nodes = list(set(tree_current) - set(self.tree_init))
        if new_nodes:
            self.lookup_status(new_nodes)

    def lookup_status(self, ids):
        def paginator(seq, rowlen):
            for start in range(0, len(seq), rowlen):
                yield seq[start:start+rowlen]
        for _ids in paginator(ids, 99):
            statuses = self.api.statuses_lookup(_ids, tweet_mode="extended")
            for status in statuses:
                db = Addstatus(status._json)
                db.addtweetdj()

    def enqueue_nodes(self, replies):
        for reply in replies:
            self.q.put(reply.id)

    def search_reply_to(
            self,
            screen_name: str,
            community: Community,
            since_id: Optional[int] = None,
    
        ):
        """Return SearchObject list containing replies to screen_name
        Replies are limited to last 7 days.
        """
        q = f"@{screen_name}"
        try:
            return self.api.search(
                q=q,
                since_id=since_id,
                include_entities=True,
                count=ReplyCrawler.max_count
            )
        except AttributeError:
            logger.error("Probable Tweepy API error.")