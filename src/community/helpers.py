import logging
from typing import Optional, List
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
from django.db.utils import DatabaseError
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import activate
from community.models import Community
from bot.tweepy_api import get_api
from moderation.models import UserCategoryRelationship, SocialMedia, SocialUser

logger = logging.getLogger(__name__)

def get_community(request):
    """
    Return a Community object or None given the request.
    """
    site = get_current_site(request)
    if not site:
        return Community.objects.first()
    try:
        return Community.objects.get(site=site.id)
    except DatabaseError:
        return
    except Community.DoesNotExist:
        site = Site.objects.first()
        if site:
            try:
                return Community.objects.get(site=site.id)
            except Community.DoesNotExist as e:
                logger.warn("Create at least one community. %s", e)
        else:
            logger.warn("Create at least one Site. %s", e)
    
def site_url(community):
    if not community:
        return
    if settings.DEBUG:
        protocol="http://"
    else:
        protocol="https://"
    return mark_safe(f"{protocol}{community.site.domain}")

def activate_language(community):
    if not community:
        return
    if not isinstance(community, Community):
        return
    language = community.language
    if not language:
        return
    activate(language)
    
def get_community_twitter_tweepy_api(community, backend=False):
    if not community:
        return
    if not isinstance(community, Community):
        return
    try:
        bot_screen_name = community.account.username
    except AttributeError:
        return
    return get_api(bot_screen_name, backend)
    
def get_community_bot_socialuser(community: Community) -> Optional[SocialUser]:
    if not community:
        return
    if not isinstance(community, Community):
        return
    try:
        user_id = community.account.userid
    except AttributeError:
        return
    try:
        su = SocialUser.objects.get(user_id=user_id)
    except SocialUser.DoesNotExist:
        return
    return su

def get_community_bot_screen_name(community: Community) -> Optional[str]:
    if not community:
        return
    if not isinstance(community, Community):
        return
    try:
        screen_name = community.account.username
    except AttributeError:
        return
    return screen_name

def get_community_member_id(community) -> Optional[List[int]]:
    if not community:
        return
    if not isinstance(community, Community):
        return
    categories = community.membership.all()
    try:
        twitter = SocialMedia.objects.get(name="twitter")
    except SocialMedia.DoesNotExist:
        return
    bot_social_user = get_community_bot_socialuser(community)
    if not bot_social_user:
        return
    member_id: List[int] = (
        UserCategoryRelationship.objects
        .filter(
            category__in=categories,
            community=community,
            social_user__social_media=twitter,
        )
        .exclude(social_user__twitter_follow_request=bot_social_user)
        .values_list("social_user__user_id", flat=True)
    )
    return member_id