# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.mail import EmailMessage
from django.template import RequestContext
from django.template import Context, Template
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from MoodDiary import models, forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request, pid=None, del_pass=None):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
        try:
            user = models.User.objects.get(username=username)
            diaries = models.Diary.objects.filter(user=user).order_by('-ddate')
        except:
            pass
    messages.get_messages(request)

    template = get_template('index.html')
    html = template.render(context=locals(), request=request)
    return HttpResponse(html)
    # years=range(1960,2020)
    # posts = models.Post.objects.filter(enabled=True).order_by('-pub_time')[:30]
    # moods = models.Mood.objects.all()
    #
    # try:
    #     user_id=request.GET['user_id']
    #     user_pass=request.GET['user_pass']
    #     user_post=request.GET['user_post']
    #     user_mood=request.GET['mood']
    #     byear=request.GET['byear']
    #     urfcolor=request.GET.getlist('fcolor')
    # except:
    #     user_id=None
    #     message='如果要张贴信息，那么每一个字段都要填...'
    #
    # if del_pass and pid:
    #     try:
    #         post=models.Post.objects.get(id=pid)
    #     except:
    #         post=None
    #
    #     if post:
    #         if post.del_pass==del_pass:
    #             post.delete()
    #             message='数据删除成功'
    #         else:
    #             message='密码错误'
    # elif user_id !=None:
    #     mood=models.Mood.objects.get(status=user_mood)
    #     post=models.Post.objects.create(mood=mood,nickname=user_id,del_pass=user_pass,message=user_post)
    #     post.save()
    #     message='成功存储！请记得您的密码[{}]!信息经审查后才能显示！'.format(user_pass)




def listing(request):
    template=get_template('listing.html')
    posts=models.Post.objects.filter(enabled=True).order_by('-pub_time')[:150]
    moods=models.Mood.objects.all()

    html=template.render(locals())
    return HttpResponse(html)


@login_required(login_url='/login/')
def posting(request):
    if request.user.is_authenticated:
        username = request.user.username
        useremail = request.user.email
    messages.get_messages(request)

    if request.method == 'POST':
        user = User.objects.get(username=username)
        diary = models.Diary(user=user)
        post_form = forms.DiaryForm(request.POST, instance=diary)
        if post_form.is_valid():
            messages.add_message(request, messages.INFO, "日记已保存")
            post_form.save()
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.INFO, '要张贴日记，每一个字段都要填...')
    else:
        post_form = forms.DiaryForm()
        messages.add_message(request, messages.INFO, '要张贴日记，每一个字段都要填...')

    template = get_template('posting.html')
    html = template.render(context=locals(), request=request)
    return HttpResponse(html)


def contact(request):
    if request.method=="POST":
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            message='感谢您的来信。'
            user_name = form.cleaned_data['user_name']
            user_city = form.cleaned_data['user_city']
            user_school = form.cleaned_data['user_school']
            user_email = form.cleaned_data['user_email']
            user_message = form.cleaned_data['user_message']
            mail_body=u'''
                网友姓名：{}
                居住城市：{}
                是否在学：{}
                反馈意见如下：{}
            '''.format(user_name,user_city,user_school,user_message)
            email=EmailMessage('来自～不吐不快～网站的网友意见',mail_body,user_email,['jianghaidi92@gmail.com'])
            email.send()
        else:
            message='请检查您输入的信息是否正确！'
    else:
        form=forms.ContactForm()
        template=get_template('contact.html')

        html = template.render(context=locals(), request=request)
        return HttpResponse(html)


def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name=request.POST['username'].strip()
            login_password=request.POST['password']
            user = authenticate(username=login_name, password=login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.add_message(request, messages.SUCCESS, '成功登录了')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, '账号尚未启用')
            else:
                messages.add_message(request, messages.WARNING, '登录失败')
        else:
            messages.add_message(request, messages.INFO,'请检查输入的字段内容')
    else:
        login_form = forms.LoginForm()

    template = get_template('login.html')
    html = template.render(context=locals(), request=request)
    response=HttpResponse(html)
    return response


def logout(request):
    auth.logout(request)
    messages.add_message(request,messages.INFO,'成功注销了！')
    return redirect('/')


@login_required(login_url='/login/')
def userinfo(request):
    if request.user.is_authenticated:
        username = request.user.username
    user = User.objects.get(username=username)
    try:
        profile = models.Profile.objects.get(user=user)
    except:
        profile = models.Profile(user=user)

    if request.method == 'POST':
        profile_form = forms.ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            messages.add_message(request, messages.INFO, "个人资料已保存")
            profile_form.save()
            return HttpResponseRedirect('/userinfo')
        else:
            messages.add_message(request, messages.INFO, '要修改个人资料，每一个字段都要填...')
    else:
        profile_form = forms.ProfileForm()

    template = get_template('userinfo.html')
    html = template.render(context=locals(), request=request)
    return HttpResponse(html)






