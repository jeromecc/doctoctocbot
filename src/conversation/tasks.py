import logging
import tweepy
from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from constance import config

from conversation.models import Retweeted, Tweetdj
from bot.models import Account
from bot.tweepy_api import get_api
from moderation.models import SocialUser
from conversation.utils import update_trees
from moderation.models import addsocialuser
from community.models import Community
from conversation.timeline import community_timeline

logger = logging.getLogger(__name__)


@shared_task
def handle_normalize(statusid):
    from .utils import normalize
    normalize(statusid)
    

@shared_task(
    soft_time_limit=config.normalize_soft_time_limit,
    time_limit=config.normalize_time_limit
)
def handle_allnormalize():
    from .utils import allnormalize
    allnormalize()

@shared_task
def handle_update_trees(hourdelta):
    update_trees(hourdelta)

@shared_task
def handle_addsocialuser():
    for instance in Tweetdj.objects.all():
        addsocialuser(instance)

@shared_task
def handle_get_physician_timeline():
    from bot.bin.timeline import record_user_timeline
    for user_id in SocialUser.objects.physician_users():
        record_user_timeline(user_id)

@shared_task
def update_retweet(days):
    """Update Retweeted and Tweetdj to reflect unretweets
    TODO: Doesn't work if the same tweet that was unretweeted is retweeted
    again.
    """
    start_datetime = timezone.now() - timedelta(days=days)
    count = 200
    for account in Account.objects.filter(active=True):
        api = get_api(username=account.username)
        if not api:
            continue
        start_tweetdj = (
            Tweetdj.objects
                .filter(socialuser__user_id=account.userid)
                .filter(created_at__gte=start_datetime)
                .last()
            )
        logger.debug(start_tweetdj)
        if not start_tweetdj:
            continue
        start_id = start_tweetdj.statusid
        timeline_status = []
        for status in tweepy.Cursor(api.user_timeline, 
                            user_id=account.userid, 
                            count=count,
                            since_id=start_id,
                            max_id=None,
                            trim_user=True,
                            exclude_replies=True,
                            include_retweets=True,
                            tweet_mode="extended",
                            ).items():
            timeline_status.append(status._json["id"])
        rt_status: List(int) = list(
            Retweeted.objects
            .filter(status__gte=start_id)
            .filter(account=account)
            .values_list("retweet", flat=True)
        )
        logger.debug(f"rt_status: {rt_status}")
        logger.debug(f"timeline_status: {timeline_status}")
        deleted = list(set(rt_status).difference(timeline_status))
        logger.debug(f"deleted: {deleted}")
        status_id = (
            Retweeted.objects
            .filter(retweet__in=deleted)
            .filter(account=account)
            .values_list('status', flat=True)
        )
        try:
            social_user = SocialUser.objects.get(user_id=account.userid)
        except SocialUser.DoesNotExist:
            social_user = None
        if social_user:
            for tweetdj in Tweetdj.objects.filter(statusid__in=status_id):
                tweetdj.retweeted_by.remove(social_user)
        
        for rt in Retweeted.objects.as_of().filter(retweet__in=deleted):
            rt.delete()
            
        for tweetdj in Tweetdj.objects.filter(statusid__in=deleted):
            if not tweetdj.deleted:
                tweetdj.deleted=True
                tweetdj.save()

@shared_task
def handle_community_members_timeline(community_name: str):
    try:
        community = Community.objects.get(name=community_name)
    except Community.DoesNotExist:
        logger.error(f"'{community_name}' does not exist.")
        return
    community_timeline(community)