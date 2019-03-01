# -*- coding: utf-8 -*-

from django import forms
from MoodDiary import models
from captcha.fields import CaptchaField
from django.forms import ModelForm
from registration.forms import RegistrationForm
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):

    class Meta:
        model = models.Profile
        fields = ['height', 'male', 'website']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['height'].label = '身高(cm)'
        self.fields['male'].label = '是男生吗'
        self.fields['website'].label = '个人网站'



class LoginForm(forms.Form):
    username = forms.CharField(label='姓名', max_length=10)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


class ContactForm(forms.Form):
    CITY=[
        ['TP',"Taipei"],
        ['TY', "Taoyuan"],
        ['TC','Taichun'],
        ['TN','Tainan'],
        ['KS','Kaosiung'],
        ['NA','Others'],
    ]
    user_name=forms.CharField(label='您的姓名',max_length=50,initial='李大仁')
    user_city=forms.ChoiceField(label='居住城市',choices=CITY)
    user_school=forms.BooleanField(label='是否在学',required=False)
    user_email=forms.EmailField(label='电子邮件')
    user_message=forms.ChoiceField(label='您的意见',widget=forms.Textarea)


class PostForm(forms.ModelForm):
    captcha=CaptchaField()
    class Meta:
        model=models.Post
        fields=['mood','nickname','message','del_pass']

    def __init__(self,*args,**kwargs):
        super(PostForm,self).__init__(*args,**kwargs)
        self.fields['mood'].label='现在的心情'
        self.fields['nickname'].label = '您的昵称'
        self.fields['message'].label = '心情留言'
        self.fields['del_pass'].label = '设置密码'
        self.fields['captcha'].label='确定您不是机器人'


# class LoginForm(forms.Form):
#     COLORS=[
#         ['红色','红色'],
#         ['橙色', '橙色'],
#         ['黄色', '黄色'],
#         ['绿色', '绿色'],
#         ['青色', '青色'],
#         ['蓝色', '蓝色'],
#         ['紫色', '紫色'],
#         ['黑色', '黑色'],
#         ['白色', '白色'],
#         ['粉色', '粉色'],
#     ]
#     user_name=forms.CharField(label='您的姓名',max_length=10)
#     user_color=forms.ChoiceField(label='幸运颜色',choices=COLORS)




class DateInput(forms.DateInput):
    input_type = 'date'


class DiaryForm(ModelForm):

    class Meta:
        model = models.Diary
        fields = ['budget', 'weight', 'note', 'ddate']
        widgets = {
            'ddate': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(DiaryForm, self).__init__(*args, **kwargs)
        self.fields['budget'].label = '今日花费(元)'
        self.fields['weight'].label = '今日体重(KG)'
        self.fields['note'].label = '心情留言'
        self.fields['ddate'].label = '日期'












