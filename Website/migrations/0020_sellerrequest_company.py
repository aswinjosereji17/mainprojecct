# Generated by Django 4.2.3 on 2023-09-07 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0019_productcategory_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellerrequest',
            name='company',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]