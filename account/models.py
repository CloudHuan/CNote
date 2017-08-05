from django.db import models

# Create your models here.
'''
CREATE TABLE User(id INT(10) PRIMARY KEY AUTO_INCREMENT,uid INT(10),name VARCHAR(100),PHOTO INT(20) UNIQUE);
'''
class User(models.Model):
    uid = models.IntegerField(default=100);
    name = models.CharField(max_length=10);
    pwd = models.CharField(max_length=200,null=False);
    phone = models.CharField(max_length=100,unique=True);

class Note(models.Model):
    uid = models.ForeignKey(User);
    content = models.TextField(max_length=500);
    cid = models.IntegerField(default=100);
    public = models.BooleanField(default=0);