# Generated by Django 2.0.10 on 2019-01-20 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crowdfunding', '0006_project_transaction_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectinvestor',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
