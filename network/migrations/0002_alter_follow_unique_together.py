# Generated by Django 4.2.4 on 2023-12-05 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('follower', 'followed')},
        ),
    ]