# Generated by Django 2.1 on 2018-09-28 01:59

from django.db import migrations


def autolog(message):
    "Automatically log the current function details."
    import inspect, logging
    # Get the previous frame in the stack, otherwise it would
    # be this function!!!
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    logging.debug("%s: %s in %s:%i" % (
        message, 
        func.co_name, 
        func.co_filename, 
        func.co_firstlineno
    ))

social_media_list = [
    'twitter',
    ]

user_id_list = [
        1020794606, # @medecinelibre 'moderator' & 'dev'
        762321963402596352, # @freehealthio 'midwife'
        2567917734, # @librehealthcare 'patient'
        2548674752, # @cryptomed 'physician' & 'moderator'
        894923722557206529, # @doctoctocbot2 'bot'
        966620293707042817, # @PharmaTocTocBot 'pharmacist'
]

categories = [
    ['physician', 'Physician', 'Médecin'],
    ['midwife', 'Midwife', 'Sage-femme'],
    ['pharmacist', 'Pharmacist', 'Pharmacien'],
    ['nurse', 'Nurse', 'IDE'],
    ['slp', 'Speech-language pathologist', 'Orthophoniste'],
    ['physical_therapist', 'Physical therapist', 'Kinésithérapeute'],
    ['medical_student', 'Medical student', 'Étudiant en médecine'],
    ['moderator', 'Moderator', 'Modérateur'],
    ['patient', 'Patient', 'Patient'],
    ['spam', 'Spam', 'Spam'],
    ['orthoptist', 'Orthoptist', 'Orthoptiste'],
    ['dentist', 'Dentist', 'Dentiste'],
    ['uap','Unlicensed assistive personnel', 'Aide-soignant'],
    ['bot', 'Robot', 'Robot'],
    ['dev', 'Developer', 'Développeur']
]

def create_socialmedia_instances(apps, schema_editor):
    SocialMedia = apps.get_model('moderation', 'SocialMedia')
    for social_media in social_media_list:
        SocialMedia.objects.get_or_create(name = social_media)

def create_category_instances(apps, schema_editor):
    Category = apps.get_model('moderation', 'Category')
    for row in categories:
        Category.objects.get_or_create(
            name = row[0],
            label_en = row[1],
            label_fr = row[2]
        )

def create_usercategoryrelationship_instances(apps, schema_editor):
    UserCategoryRelationship = apps.get_model('moderation', 'UserCategoryRelationShip')
    Category = apps.get_model('moderation', 'Category')
    SocialUser = apps.get_model('moderation', 'SocialUser')
    SocialMedia = apps.get_model('moderation', 'SocialMedia')
    
    soc_med_obj, _ = SocialMedia.objects.get_or_create(name = 'twitter')
    
    mod_cat_obj, _ = Category.objects.get_or_create(name='moderator')
    spam_cat_obj, _ = Category.objects.get_or_create(name='spam')
    midwife_cat_obj, _ = Category.objects.get_or_create(name='midwife')
    patient_cat_obj, _ = Category.objects.get_or_create(name='patient')
    physician_cat_obj, _ = Category.objects.get_or_create(name='physician')
    pharmacist_cat_obj, _ = Category.objects.get_or_create(name='pharmacist')
    bot_cat_obj, _ = Category.objects.get_or_create(name='bot')
    dev_cat_obj, _ = Category.objects.get_or_create(name='dev')

    # 1020794606 @medecinelibre 'moderator'
    social_user_obj, _ = SocialUser.objects.get_or_create(user_id = 1020794606, social_media = soc_med_obj)
    moderator = social_user_obj
    user_category_relationship = UserCategoryRelationship(
        social_user = social_user_obj,
        category = mod_cat_obj,
        moderator = moderator
    )
    user_category_relationship.save
    
    # 1020794606 @medecinelibre 'dev'
    social_user_obj, _ = SocialUser.objects.get_or_create(user_id = 1020794606, social_media = soc_med_obj)
    moderator = social_user_obj
    user_category_relationship = UserCategoryRelationship(
        social_user = social_user_obj,
        category = dev_cat_obj,
        moderator = moderator
    )
    user_category_relationship.save

    #894923722557206529 @doctoctocbot2 'bot'
    social_user_obj, _ = SocialUser.objects.get_or_create(user_id = 894923722557206529, social_media = soc_med_obj)
    user_category_relationship, _ = UserCategoryRelationship.objects.get_or_create(
        social_user = social_user_obj,
        category = bot_cat_obj,
        moderator = moderator)

    # 762321963402596352 @freehealthio 'midwife'
    social_user_obj, _ = SocialUser.objects.get_or_create(user_id = 762321963402596352, social_media = soc_med_obj)
    UserCategoryRelationship.objects.get_or_create(
        social_user = social_user_obj,
        category = midwife_cat_obj,
        moderator = moderator
    )

    # 2567917734, @librehealthcare 'patient'
    social_user_obj, _ = SocialUser.objects.get_or_create(user_id = 2567917734, social_media = soc_med_obj)
    UserCategoryRelationship.objects.get_or_create(
        social_user = social_user_obj,
        category = patient_cat_obj,
        moderator = moderator
    )
    user_category_relationship.save()

    # 2548674752, @cryptomed 'physician' & 'moderator'
    social_user_obj, _ = SocialUser.objects.get_or_create(user_id = 2548674752, social_media = soc_med_obj)
    UserCategoryRelationship.objects.get_or_create(
        social_user = social_user_obj,
        category = physician_cat_obj,
        moderator = moderator
    )
    UserCategoryRelationship.objects.get_or_create(
        social_user = social_user_obj,
        category = mod_cat_obj,
        moderator = moderator
    )

    # 966620293707042817, @PharmaTocTocBot 'pharmacist'
    social_user_obj, _ = SocialUser.objects.get_or_create(user_id = 966620293707042817, social_media = soc_med_obj)
    UserCategoryRelationship.objects.get_or_create(
        social_user = social_user_obj,
        category = pharmacist_cat_obj,
        moderator = moderator
    )
               
class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_socialmedia_instances, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(create_category_instances, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(create_usercategoryrelationship_instances, reverse_code=migrations.RunPython.noop),
    ]
