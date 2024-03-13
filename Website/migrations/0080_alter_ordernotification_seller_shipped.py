# Generated by Django 4.2.6 on 2024-02-21 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0079_useraddress_city_useraddress_district_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordernotification_seller',
            name='shipped',
            field=models.CharField(choices=[('OR', 'Order Requested'), ('DL', 'Delivered'), ('SU', 'Successful')], default='OR', max_length=2),
        ),
    ]