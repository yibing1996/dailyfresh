from django.db import models

class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemial = models.CharField(max_length=30)
    ushow = models.CharField(max_length=20)
    uaddress = models.CharField(max_length=100)
    uyoubian = models.CharField(max_length=7)
    uphone = models.CharField(max_length=11)


