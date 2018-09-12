#coding=utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponseRedirect
from hashlib import sha1
from models import *
from df_goods.models import *
import user_decorator


def register(request):
    context = {
        'page_name': 1,
        'title': '用户注册',
    }
    return render(request, 'df_user/register.html', context)


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def register_handle(request):
    # 接收页面信息
    post = request.POST
    uname = post['user_name']
    upwd = post['pwd']
    ucpwd = post['cpwd']
    uemail = post['email']

    # 加密密码
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    # 判读两次密码是否一样
    if upwd != ucpwd:
        return redirect('/user/register')

    # 保存到数据库中
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemial = uemail
    user.save()

    return redirect('/user/login')


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {
        'page_name': 1,
        'title': '用户登录',
        'error_name': 0,
        'error_pwd': 0,
        'uname': uname,
    }
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    # 获取用户登录信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)

    # 根据用户名在数据库中查询用户的相关信息
    users = UserInfo.objects.filter(uname=uname)

    # 查询到用户名
    if len(users) == 1:
        upwd1 = users[0].upwd
        s1 = sha1()
        s1.update(upwd)
        upwd2 = s1.hexdigest()

        # 判断用户输入的密码和数据库中的密码是否相同
        if upwd1 == upwd2:
            url=request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)
            if jizhu == 1:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red

        # 即用户密码输入错误
        else:
            context = {
                'page_name': 1,
                'title': '用户登录',
                'error_name': 0,
                'error_pwd': 1,
                'uname': uname,
                 'upwd': upwd,
            }
            return render(request, 'df_user/login.html', context)

    # 没有查询到用户名
    else:
        context = {
            'page_name': 1,
            'title': '用户登录',
            'error_name': 1,
            'error_pwd': 0,
            'uname': uname,
            'upwd': upwd,
        }
        return render(request, 'df_user/login.html', context)


@user_decorator.login
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemial
    # 最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    for goods_id in goods_ids1:
        goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {
        'page_name': 1,
        'title': '用户中心',
        'user_email': user_email,
        'user_name': request.session['user_name'],
        'goods_list': goods_list
    }
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def order(request):
    context = {
        'page_name': 1,
        'title': '用户中心'
    }
    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushow = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {
        'page_name': 1,
        'title': '用户中心',
        'user': user,
    }
    return render(request, 'df_user/user_center_site.html', context)



def logout(request):
    request.session.flush()
    return redirect('/')




