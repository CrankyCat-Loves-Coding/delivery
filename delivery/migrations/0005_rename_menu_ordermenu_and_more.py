# Generated by Django 4.0.4 on 2022-05-21 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_customer_order_alter_menu_description_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Menu',
            new_name='OrderMenu',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='menu',
            new_name='ordermenu',
        ),
    ]
