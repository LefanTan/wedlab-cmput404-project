# Generated by Django 4.0.2 on 2022-04-02 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_alter_likecomment_id_alter_likepost_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='likecomment',
            name='post',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='likepost',
            name='post',
            field=models.CharField(max_length=500, null=True),
        ),
    ]