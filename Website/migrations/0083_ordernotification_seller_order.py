# Generated by Django 4.2.6 on 2024-02-21 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0082_ordernotification_seller_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordernotification_seller',
            name='order',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Website.orderitem'),
        ),
    ]
