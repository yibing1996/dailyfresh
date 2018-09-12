from django.db import models
from df_user.models import UserInfo
from df_goods.models import GoodsInfo


class CartInfo(models.Model):
    user = models.ForeignKey(UserInfo)
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()
