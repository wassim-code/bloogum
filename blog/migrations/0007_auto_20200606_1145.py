# Generated by Django 3.0.7 on 2020-06-06 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_comment_pub_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='likes',
        ),
    ]
