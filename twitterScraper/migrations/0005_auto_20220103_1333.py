# Generated by Django 3.2.6 on 2022-01-03 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitterScraper', '0004_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tweet',
            old_name='keyword_polarity_date',
            new_name='keyword_data',
        ),
        migrations.AddField(
            model_name='tweet',
            name='until',
            field=models.CharField(default=' ', max_length=50),
        ),
    ]