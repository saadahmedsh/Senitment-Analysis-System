from email.policy import default
from django.db import models
from django.db.models.expressions import When


# Create your models here.


class tweet(models.Model):
    keyword_id=models.AutoField(primary_key=True)
    keyword=models.CharField(max_length=100, unique=True)
    since=models.CharField(max_length=50, default=' '), 
    until=models.CharField(max_length=50, default=' ')
    keyword_data=models.JSONField()
    prediction=models.JSONField(dict())

    
    

class user(models.Model):
    user_id=models.AutoField(primary_key=True)
    user_email=models.EmailField(unique=True)
    user_password=models.CharField(max_length=50)


