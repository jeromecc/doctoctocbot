# Generated by Django 2.2.4 on 2019-12-11 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfunding', '0005_project_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectinvestment',
            name='invoice',
            field=models.PositiveIntegerField(blank=True, default=None, help_text='Id of the invoice in the billing app.', null=True, unique=True),
        ),
    ]
