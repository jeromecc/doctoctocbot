from typing import List

from rest_framework import serializers
from .models import Hashtag, Tweetdj
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
from display.views import (
    get_biggeravatar_url,
    get_normalavatar_url,
    get_miniavatar_url,
)
from users.utils import get_api_level
from community.helpers import get_community
from community.models import ApiAccess
from users.utils import get_all_categories_from_social_user
from community.helpers import activate_language
from moderation.models import SocialUser
from tagging.models import Category


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = ('hashtag',)
        

class TweetdjSerializer(TaggitSerializer, serializers.ModelSerializer):
    avatar_normal = serializers.SerializerMethodField()
    avatar_mini = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_screen_name = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    id_str = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    author_category = serializers.SerializerMethodField()
    author_specialty = serializers.SerializerMethodField()
    status_category = serializers.SerializerMethodField()
    status_tag = serializers.SerializerMethodField()

    
    class Meta:
        model = Tweetdj
        fields = (
            'statusid',
            'id_str',
            'socialuser',
            'user_name',
            'user_screen_name',
            'created_at',
            'text',
            'avatar_normal',
            'avatar_mini',
            'author_category',
            'author_specialty',
            'status_category',
            'status_tag',
        )

    def get_id_str(self, obj):
        try:
            return obj.json['id_str']
        except TypeError:
            return ""

    def get_avatar_normal(self, obj):
        return get_normalavatar_url(obj.userid)
    
    def get_avatar_mini(self, obj):
        return get_miniavatar_url(obj.userid)
    
    def get_user_name(self, obj):
        try:
            return obj.json['user']['name']
        except TypeError:
            return ""

    def get_user_screen_name(self, obj):
        try:
            return obj.json['user']['screen_name']
        except TypeError:
            return ""

    def get_created_at(self, obj):
        try:
            return obj.json['created_at']
        except TypeError:
            return ""

    def get_text(self, obj):
        try:
            return obj.json['full_text']
        except TypeError:
            try:
                return obj.json['text']
            except TypeError:
                return ""

    def get_author_category(self, obj):
        api_access = get_api_access(self.context['request'])
        if api_access and api_access.author_category:
            author_id = obj.json['user']['id']
            community = get_community(self.context['request'])
            try:
                su = SocialUser.objects.get(user_id=author_id)
            except SocialUser.DoesNotExist:
                return
            categories = get_all_categories_from_social_user(su, community)
            activate_language(community)
            return [category.label for category in categories]

    def get_author_specialty(self, obj):
        pass
    
    def get_status_category(self, obj):
        api_access = get_api_access(self.context['request'])
        if api_access and api_access.status_category:
            status_id = obj.json['id']
            community = get_community(self.context['request'])
            try:
                tweetdj = Tweetdj.objects.get(statusid=status_id)
            except Tweetdj.DoesNotExist:
                return  
            return list(
                tweetdj.tags
                .filter(pk__in=tagging_categories_id(community))
                .values_list("name", flat=True)
            )

    def get_status_tag(self, obj):
        api_access = get_api_access(self.context['request'])
        if api_access and api_access.status_tag:
            status_id = obj.json['id']
            community = get_community(self.context['request'])
            try:
                tweetdj = Tweetdj.objects.get(statusid=status_id)
            except Tweetdj.DoesNotExist:
                return  
            return list(
                tweetdj.tags
                .exclude(pk__in=tagging_categories_id(community))
                .values_list("name", flat=True)
            )


def tagging_categories_id(community) -> List[int]:
    return list(
        Category.objects.filter(is_category=True, community=community)
        .values_list("taggit_tag__pk", flat=True)
    )

def get_api_access(request):
        community = get_community(request)
        api_level = get_api_level(
            request.user,
            community
        )
        try:
            return ApiAccess.objects.get(
                community=community,
                level = api_level,
            )
        except ApiAccess.DoesNotExist:
            return