# Generated by Django 3.2 on 2022-05-21 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_auto_20220521_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
