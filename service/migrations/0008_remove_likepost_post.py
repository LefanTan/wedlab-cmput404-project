# Generated by Django 4.0.2 on 2022-04-02 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_likecomment_post_likepost_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likepost',
            name='post',
        ),
    ]