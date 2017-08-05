from django.db import models

# Create your models here.

class User(models.Model):
    uid = models.IntegerField(default=0);
    name = models.CharField(max_length=10,unique=True);
    pwd = models.CharField(max_length=200);
    phone = models.CharField(max_length=100,unique=True);
    token = models.CharField(max_length=100);

class Note(models.Model):
    #uid = models.ForeignKey(User);
    uuid = models.IntegerField(default=0);
    content = models.TextField();
    cid = models.IntegerField(default=0);
    public = models.BooleanField(default=False);

