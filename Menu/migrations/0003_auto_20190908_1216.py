# Generated by Django 2.2.5 on 2019-09-08 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Menu', '0002_auto_20190906_1950'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='depth',
            new_name='level',
        ),
    ]
