# Generated by Django 4.2.4 on 2023-10-30 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_rename_user_id_listing_user_bid_listing_bid_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
