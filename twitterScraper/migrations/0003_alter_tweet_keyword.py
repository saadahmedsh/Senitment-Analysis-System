# Generated by Django 3.2.6 on 2021-12-31 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitterScraper', '0002_delete_temp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='keyword',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
