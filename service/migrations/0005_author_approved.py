# Generated by Django 4.0.2 on 2022-03-31 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0004_merge_20220323_0701'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
