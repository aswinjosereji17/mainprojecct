# Generated by Django 4.2.6 on 2024-01-19 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0062_delete_subscription_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_name', models.CharField(max_length=255)),
                ('sub_image', models.CharField(max_length=255)),
                ('sub_amount', models.FloatField()),
                ('sub_offer1', models.CharField(max_length=255)),
                ('sub_offer2', models.CharField(max_length=255)),
                ('sub_offer3', models.CharField(max_length=255)),
            ],
        ),
    ]