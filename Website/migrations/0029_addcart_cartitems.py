# Generated by Django 4.2.3 on 2023-09-13 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Website', '0028_alter_useraddress_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddCart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('cart_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItems',
            fields=[
                ('cart_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('cart_item_date', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Website.addcart')),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Website.product')),
            ],
        ),
    ]