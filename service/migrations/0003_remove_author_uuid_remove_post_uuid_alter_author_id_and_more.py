# Generated by Django 4.0.2 on 2022-02-23 20:59

from django.db import migrations, models
import service.models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_alter_post_contenttype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='post',
            name='uuid',
        ),
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.CharField(default=service.models.generate_uuid_hex, max_length=250, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.CharField(default=service.models.generate_uuid_hex, max_length=250, primary_key=True, serialize=False),
        ),
    ]
