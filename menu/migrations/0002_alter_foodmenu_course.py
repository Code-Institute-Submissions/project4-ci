# Generated by Django 3.2 on 2022-06-07 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodmenu',
            name='course',
            field=models.IntegerField(choices=[('s', 'Starters'), ('m', 'Mains'), ('d', 'Desert')]),
        ),
    ]
