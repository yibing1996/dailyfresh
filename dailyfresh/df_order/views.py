# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render, redirect
from df_user import user_decorator
from df_user.models import *
from df_cart.models import *
from django.db import transaction
from models import *
from datetime import datetime
from decimal import Decimal

@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id=transaction.savepoint()
    # 接收购物车编号
    cart_ids = request.POST.get('cart_ids')
    try:
        # 创建订单对像
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d'% (now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = now
        order.ototal=Decimal(request.POST.get('total'))
        order.save()
        # 创建详单对像
        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        for id1 in cart_ids:
            detail = OrderDetailInfo()
            detail.order = order
            # 查询购物车信息
            cart = CartInfo.objects.get(id=id1)
            # 判断商品库存
            goods = cart.goods
            if goods.gkucun >= cart.count: # 如果库存大于购买数量
                # 减少商品库存
                goods.gkucun=cart.goods.gkucun-cart.count
                goods.save()
                # 完善详单信息
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                # 删除购物车数据
                cart.delete()
            else: # 如果库存小于购买数量
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
        transaction.savepoint_commit(tran_id)

    except Exception as e:
        print '==========%s' % e
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/order/')










