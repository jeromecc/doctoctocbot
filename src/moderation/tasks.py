import os
import random
import time
from unicodedata import category

from versions.exceptions import DeletionOfNonCurrentVersionError

from celery import shared_task
from bot.bin.user import getuser_lst
from .profile import twitterprofile
from moderation.lists.poll import poll_lists_members, create_update_lists
from django.conf import settings
from conversation.utils import screen_name

from django.utils.translation import activate
from django.db import transaction, DatabaseError
from dm.models import DirectMessage
from moderation.models import (
    Moderation,
    SocialUser,
    Category,
    UserCategoryRelationship,
    CategoryMetadata,
    Moderator,
    Queue,
)

from common.utils import trim_grouper
from django.utils.translation import gettext as _
from moderation.social import send_graph_dm
from bot.onstatus import triage_status

from moderation.moderate import quickreply
from dm.api import senddm
from community.models import Community
from moderation.profile import check_profile_pictures
from moderation.profile import (
    create_update_profile_twitter,
    create_update_profile_local,
    )
from community.helpers import activate_language
from moderation.social import update_social_ids
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def handle_poll_lists_members(community_name: str):
    poll_lists_members(community_name)
    

@shared_task
def handle_create_update_lists(community_name: str):
    create_update_lists(community_name)

@shared_task
def handle_create_update_profile(userid: int):
    try:
        su: SocialUser = SocialUser.objects.get(user_id=userid)
    except SocialUser.DoesNotExist:
        return
    try:
        sm: SocialMedia = su.social_media
    except AttributeError:
        return
    if sm.name == 'twitter':
        create_update_profile_twitter(su)
    elif sm.name == settings.THIS_SOCIAL_MEDIA:
        create_update_profile_local(su)

def handle_create_all_profiles():
    from conversation.models import Tweetdj
    su_qs_lst = SocialUser.objects.values('user_id', 'profile')
    user_id_request_lst = []
    
    for su in su_qs_lst:
        if not su["profile"]:
            try:
                tweetdj_mi = Tweetdj.objects.filter(userid = su["user_id"]).latest()
            except Tweetdj.DoesNotExist:
                user_id_request_lst.append(su["user_id"])
                continue
            userjson = tweetdj_mi.json.get("user")
            twitterprofile(userjson)
    
    if user_id_request_lst:
        for user_id_lst in trim_grouper(user_id_request_lst, 100):
            user_jsn_lst = getuser_lst(user_id_lst)
            if not user_jsn_lst:
                continue
            for user_jsn in user_jsn_lst:
                twitterprofile(user_jsn)

@shared_task
def handle_check_all_profile_pictures():
    userid_lst = SocialUser.objects.values_list('user_id', flat=True)
    for userid in userid_lst:
        check_profile_pictures(userid)

@shared_task(bind=True, max_retries=2)
def handle_sendmoderationdm(self, mod_instance_id):
    logger.debug("inside handle_sendmodarationdm()")
    
    # community
    try:
        mod_mi = Moderation.objects.get(pk=mod_instance_id)
    except Moderation.DoesNotExist:
        logger.error(f"Moderation with id={id} does not exist.")
        return

    handle_create_update_profile.apply_async(args=(mod_mi.queue.user_id,))

    # select language
    try:
        community = mod_mi.queue.community
    except:
        community = None
    activate_language(community)

    qr = quickreply(mod_instance_id)
    logger.debug(f"qr:{qr}")
    logger.info(f"mod_mi.moderator.user_id: {mod_mi.moderator.user_id}")
    #logger.debug(f"moderator profile: {mod_mi.moderator.profile}")
    logger.info(f"mod_mi.queue.user_id {mod_mi.queue.user_id}")
    sn = screen_name(mod_mi.queue.status_id)
    status_id = mod_mi.queue.status_id

    dm_txt = (_("Please verify this user: @{screen_name} "
              "Tweet: https://twitter.com/{screen_name}/status/{status_id}")
              .format(screen_name=sn, status_id=status_id))
    logger.debug(f"dm_txt: {dm_txt}")
    
    # social graph DM
    ok = send_graph_dm(
        mod_mi.queue.user_id,
        mod_mi.moderator.user_id,
        mod_mi.queue.community.account.username,
        _("You will soon receive a verification request for this user."),
        mod_mi.queue.community
    )
    logger.info(f"graph: {ok}")

    # verification DM
    ok = senddm(
        dm_txt,
        user_id=mod_mi.moderator.user_id,
        screen_name=mod_mi.queue.community.account.username,
        return_json=True,
        quick_reply=qr
    )
    logger.info(f"dm:{ok}")

@shared_task
def poll_moderation_dm():

    def get_moderation_metadata(dm):
        return dm.jsn['kwargs']['message_create']['message_data']['quick_reply_response']['metadata']
    
    def get_moderation_id(dm):
        return get_moderation_metadata(dm)[10:46]
    
    def get_moderation_category_name(dm):
        return get_moderation_metadata(dm)[46:]
    
    current_mod_uuids = [str(mod.id) for mod in Moderation.objects.current.filter(state=None)]
    logger.debug(f"current_mod_uuids: {current_mod_uuids}")
    # return if no current Moderation object
    if not current_mod_uuids:
        return
    bot_id_lst = Community.objects.values_list("account__userid", flat=True)
    #logger.info(f"current_moderations_uuid_str_lst: {current_moderations_uuid_str_lst}")
    dms = DirectMessage.objects\
        .filter(recipient_id__in=bot_id_lst)\
        .filter(jsn__kwargs__message_create__message_data__quick_reply_response__metadata__startswith="moderation")
    logger.info(f"all moderation direct messages answers: {len(dms)} {[dm.text + os.linesep for dm in dms]}")
    #dmsgs_current = [dmsg for dmsg in dmsgs if (dmsg.jsn['kwargs']['message_create']['message_data']['quick_reply_response']['metadata'].split("_")[1] in current_moderations_uuid_str_lst)]

    dms_current = []
    for dm in dms:
        uid = get_moderation_id(dm)
        logger.info(f"uid: {uid}")
        ok = uid in current_mod_uuids
        logger.info(f"ok = uid in current_mod_uuids: {ok}")
        if ok:
            dms_current.append(dm)
    
    #logger.info(f"current moderation direct messages answers: {len(dms_current)} {[dm.text + os.linesep for dm in dms_current]}")
    for dm in dms_current:
        moderation_id = get_moderation_id(dm)
        mod_cat_name = get_moderation_category_name(dm)
        logger.info(f"dm moderation_id: {moderation_id}, cat: {mod_cat_name}")
        #retrieve moderation instance
        try:
            mod_mi = Moderation.objects.get(id=moderation_id)
        except Moderation.DoesNotExist as e:
            logger.error(f"Moderation object with id {moderation_id} "
                         f"does not exist. Error message: {e}")
            continue
        logger.info(f"mod_mi:{mod_mi}")
        # if mod_mi is not the current version, current_version() returns None
        # and it means this moderation was already done and we pass
        is_current = bool(Moderation.objects.current_version(mod_mi))
        if not is_current:    
            logger.info(f"Moderation instance {mod_mi} was already moderated.")
            continue
        
        # determine id of moderated user
        su_id_int = mod_mi.queue.user_id
        
        # moderated SocialUser instance
        try:
            moderated_su_mi = SocialUser.objects.get(user_id=su_id_int)
            logger.info(f"moderated_su_mi:{moderated_su_mi}")
            logger.info(f"moderated_su_mi.profile:{moderated_su_mi.profile}")
        except SocialUser.DoesNotExist:
            continue
        
        # Category (cat_mi) or CategoryMetadata (meta_mi) model instance
        try:
            cat_mi = Category.objects.get(name=mod_cat_name)
            logger.info(f"cat_mi:{cat_mi}")
        except Category.DoesNotExist:
            cat_mi = None
            try:
                meta_mi = CategoryMetadata.objects.get(name=mod_cat_name)
                logger.info(f"meta_mi:{meta_mi}")
            except CategoryMetadata.DoesNotExist:
                continue
        # moderator SocialUser instance
        try:
            moderator_su_mi = SocialUser.objects.get(user_id=dm.sender_id)
            logger.info(f"moderator_su_mi:{moderator_su_mi}")
        except SocialUser.DoesNotExist:
            continue
        if cat_mi:
            process_cat_mi(cat_mi, moderated_su_mi, moderator_su_mi, mod_mi)
        elif meta_mi:
            process_meta_mi(meta_mi, moderated_su_mi, moderator_su_mi, mod_mi)

def delete_moderation_queue(mod_mi):
    with transaction.atomic():
        try:
            mod_mi.queue.delete()
        except DeletionOfNonCurrentVersionError as e:
            logger.info(f"Queue {mod_mi.queue} was already deleted. %s" % e)
        try:
            mod_mi.delete()
        except DeletionOfNonCurrentVersionError as e:
            logger.info(f"Moderation instance {mod_mi} was already moderated. %s" % e)

def process_cat_mi(cat_mi, moderated_su_mi, moderator_su_mi, mod_mi):        
    #Check if relationship already exists for the given community
    #if cat_mi in moderated_su_mi.category.all():
    if (moderated_su_mi.categoryrelationships
        .filter(community=mod_mi.queue.community,category=cat_mi)
        .exclude(moderator=moderated_su_mi)
        .exists()):
        logger.info(f"{moderated_su_mi} is already a {cat_mi} for community {mod_mi.queue.community}")
        with transaction.atomic():
            mod_mi.state = get_category_metadata_done()
            mod_mi.save()
        delete_moderation_queue(mod_mi)
        return
    # TODO: check if there exists a categoryrelationship created by another
    # community where cat_mi differs and warn both communities of the discrepancy
 
    # create UserCategoryRelationship
    ucr = None
    with transaction.atomic():
        try:
            ucr = UserCategoryRelationship.objects.create(
              social_user = moderated_su_mi,
              category = cat_mi,
              moderator = moderator_su_mi,
              community = mod_mi.queue.community
            )
        except DatabaseError as e:
            logger.error(e)
            return
    if ucr:
        logger.info(f"ucr creation successful: {ucr}")
        mod_mi.state = get_category_metadata_done()
        mod_mi.save()
        mod_mi.delete()
        status_id = mod_mi.queue.status_id
        # delete queue object corresponding to this moderation
        delete_moderation_queue(mod_mi)
        # send status to triage, it will be retweeted according to retweet rules of communities
        triage_status(status_id)
        # TODO: create a cursor based on DM timestamp to avoid processing all DMs during each polling
        # TODO: check that the moderator is following the bot before attempting to send a DM

def process_meta_mi(meta_mi, moderated_su_mi, moderator_su_mi, mod_mi):
    """Process meta moderation anwsers such as 'stop', 'fail' or 'busy'
    """
    queue= mod_mi.queue
    if not queue:
        return
    community=queue.community
    if not community:
        return
    if meta_mi.name == "stop":
        logger.debug(f"SocialUser {moderator_su_mi} wants to stop.")
        # clone moderation instance, change its state to 'stop', then delete it
        with transaction.atomic():
            mod_mi.state = meta_mi
            mod_mi.save()
            mod_mi.delete()
        # make moderator inactive
        moderator_mi = moderator_su_mi.moderator.filter(
            active=True,
            community=community
        ).first()
        if moderator_mi:
            moderator_mi.public=False
            moderator_mi.active=False
            moderator_mi.save()
        # create new moderation
        create_moderation(
            community,
            queue,
        )
    elif meta_mi.name == "fail":
        logger.debug(f"SocialUser {moderator_su_mi}: fail")
        # clone moderation instance and change its state to 'fail'
        with transaction.atomic():
            mod_mi.state = meta_mi
            mod_mi.save()
            mod_mi.delete()
        # create new moderation with senior moderator
        create_moderation(
            community,
            queue,
            senior=True,
        )
    elif meta_mi.name == "busy":
        logger.debug(f"SocialUser {moderator_su_mi} is busy.")
        # clone moderation instance and change its state to 'busy'
        with transaction.atomic():
            mod_mi.state = meta_mi
            mod_mi.save()
            mod_mi.delete()
        # create new moderation excluding this busy social_user
        create_moderation(
            community,
            queue,
            exclude=moderator_su_mi,
            senior=False,
        )

def create_moderation(community, queue, exclude=None, senior=False):
    qs = Moderator.objects.filter(
        community=community,
        active=True,
    )
    if senior:
        qs= qs.filter(senior=True)
    logger.debug(f"create_moderation QuerySet (before excluding {exclude}): {qs}")
    if isinstance(exclude, SocialUser):
        qs=qs.exclude(socialuser=exclude)
    logger.debug(f"create_moderation QuerySet (after excluding {exclude}): {qs}")
    random.seed(os.urandom(128))
    new_moderator_mi = random.choice(list(qs))
    logger.debug(f"new_moderator_mi: {new_moderator_mi}")
    try:
        new_mod_mi = Moderation.objects.create(
            moderator = new_moderator_mi.socialuser,
            queue = queue,
        )
        logger.debug(f"new_mod_mi: {new_mod_mi}")
    except:
        return
    
def get_category_metadata_done():
    try:
        return CategoryMetadata.objects.get(name='done')
    except CategoryMetadata.DoesNotExist:
        return None

@shared_task
def update_moderators_friends():
    for dct in Moderator.objects.filter(active=True).values(
        'socialuser',
        'community'
    ).order_by('socialuser__id').distinct('socialuser'):
        su = SocialUser.objects.get(id=dct["socialuser"])
        community = Community.objects.get(id=dct["community"])
        update_social_ids(
            su,
            cached=False,
            bot_screen_name=community.account.username,
            relationship='friends',
        )
        time.sleep(settings.API_FRIENDS_PERIOD)