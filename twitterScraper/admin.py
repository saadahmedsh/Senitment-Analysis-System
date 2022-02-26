from django.contrib import admin
import twitterScraper.models as model
# Register your models here.



admin.site.register(model.tweet)
admin.site.register(model.user)
