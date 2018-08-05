from django.db import models

class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemial = models.CharField(max_length=30)
    ushow = models.CharField(max_length=20, default='')
    uaddress = models.CharField(max_length=100, default='')
    uyoubian = models.CharField(max_length=7, default='')
    uphone = models.CharField(max_length=11, default='')


