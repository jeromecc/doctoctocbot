from django.contrib import admin
from versions.admin import VersionedAdmin

from .models import SocialUser, UserCategoryRelationship, Category, Profile, Queue, Moderation, TwitterList


class CategoryRelationshipInline(admin.TabularInline):
    model = UserCategoryRelationship
    extra = 10
    fk_name = 'category'
    raw_id_fields = ("social_user", "moderator",)
    
    def screen_name_tag(self, obj):
        screen_name = obj.social_user.profile.json.get("screen_name", None)
        return screen_name
    
    screen_name_tag.short_description = 'Screen name'
    readonly_fields = ('screen_name_tag',)

    
class UserRelationshipInline(admin.TabularInline):
    model = UserCategoryRelationship
    extra = 10
    fk_name = 'social_user'


class SocialUserAdmin(admin.ModelAdmin):
    inlines = (UserRelationshipInline,)
    list_display = ('mini_image_tag', 'screen_name_tag', 'name_tag', 'user_id', 'social_media', )
    fields = ('normal_image_tag', 'screen_name_tag', 'name_tag', 'user_id', 'social_media',)
    readonly_fields = ('normal_image_tag', 'screen_name_tag', 'name_tag', 'user_id', 'social_media',)
    search_fields = ('user_id',)

class CategoryAdmin(admin.ModelAdmin):
    inlines = (CategoryRelationshipInline,)
    fields = ('name', 'label',)

    
class QueueAdmin(VersionedAdmin):
    pass
    list_display = ('mini_image_tag', 'screen_name_tag', 'name_tag', 'status_tag', 'user_id',)
    readonly_fields = ('mini_image_tag', 'screen_name_tag', 'name_tag', 'status_tag', 'user_id', 'status_id',)
    list_display_show_identity = False
    list_display_show_end_date = False
    list_display_show_start_date = True


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('mini_image_tag', 'screen_name_tag', 'name_tag', 'socialuser',)
    fields = ('mini_image_tag', 'screen_name_tag', 'name_tag', 'socialuser', 'json',)
    readonly_fields = ('mini_image_tag', 'screen_name_tag', 'name_tag', 'socialuser', 'json',)


class ModerationAdmin(VersionedAdmin):
    pass
    list_display = ('moderator_mini_image_tag', 'moderator_screen_name_tag', 'moderated_mini_image_tag', 'moderated_screen_name_tag', 'status_tag',)
    fields = ('moderator_mini_image_tag',
              'moderator_screen_name_tag',
              'moderated_mini_image_tag',
              'moderated_screen_name_tag',
              'status_tag',
              'id',
              'identity',
              )
    readonly_fields = ('moderator_mini_image_tag', 'moderator_screen_name_tag', 'moderated_mini_image_tag', 'moderated_screen_name_tag', 'status_tag',)
    list_display_show_identity = True
    list_display_show_end_date = True
    list_display_show_start_date = True


class TwitterListAdmin(admin.ModelAdmin):
    list_display = (
        'list_id',
        'slug',
        'name',
        'twitter_description',
        'uid',
        'label',
        'local_description',
    )
    fields = (
        'list_id',
        'slug',
        'name',
        'twitter_description',
        'uid',
        'label',
        'local_description',
        'json'    
    )
    readonly_fields = (
        'list_id',
        'slug',
        'name',
        'twitter_description',
        'json'    
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(SocialUser, SocialUserAdmin)

admin.site.register(Profile, ProfileAdmin)

admin.site.register(Queue, QueueAdmin)
admin.site.register(Moderation, ModerationAdmin)
admin.site.register(TwitterList, TwitterListAdmin)