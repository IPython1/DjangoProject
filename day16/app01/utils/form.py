from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms

from app01.models import UserInfo, PrettyNum, Admin
from app01.utils.bootstrap import BootStrapModelForm, BootStrapForm
from app01.utils.encrypt import md5

class LoginForm(BootStrapForm):
    name=forms.CharField(
        label='用户名',
        widget=forms.TextInput
    )
    password=forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True)
    )
    code=forms.CharField(
        label='验证码',
        widget=forms.TextInput
    )


    def clean_password(self):
        pwd=self.cleaned_data.get('password')
        return md5(pwd)
class LoginModelForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['name', 'password']
class AdminModelForm(BootStrapModelForm):
    # # 验证规则 方式一 字段+正则
    name = forms.CharField(min_length=2, max_length=100, label="用户名")
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = Admin
        fields = ('name','password','confirm_password')
        widgets={
            "password": forms.PasswordInput(render_value=True),
        }
    def clean_password(self):
        pwd = self.cleaned_data['password']

        return md5(pwd)
    def clean_confirm_password(self):
        print(self.cleaned_data['password'])
        pwd = self.cleaned_data['password']
        confirm = md5(self.cleaned_data['confirm_password'])
        if pwd != confirm:
            raise ValidationError('密码不一致，请重新输入')
        #返回什么，此字段以后保存到数据库的就是什么
        return confirm
class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = Admin
        fields = ['name']
class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput,
    )
    class Meta:
        model = Admin
        fields = ['password','confirm_password']
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }
    def clean_password(self):
        pwd = self.cleaned_data['password']

        return md5(pwd)
    def clean_confirm_password(self):
        print(self.cleaned_data['password'])
        pwd = self.cleaned_data['password']
        confirm = md5(self.cleaned_data['confirm_password'])
        if pwd != confirm:
            raise ValidationError('密码不一致，请重新输入')
        #返回什么，此字段以后保存到数据库的就是什么
        return confirm
class UserModelForm(BootStrapModelForm):
    # # 验证规则 方式一 字段+正则
    name = forms.CharField(min_length=2, max_length=100, label="用户名")
    class Meta:
        model = UserInfo
        fields = ('name','password','age','account','gender','depart')
        # widgets={
        #     "name":forms.TextInput(attrs={'class':'form-control'}),
        #     "password":forms.PasswordInput(attrs={'class':'form-control'}),
        #     "age":forms.TextInput(attrs={'class':'form-control'}),
        #     "account":forms.TextInput(attrs={'class':'form-control'}),
        #     "gender":forms.Select(attrs={'class':'form-control'}),
        #     "depart":forms.Select(attrs={'class':'form-control'}),
        # }
class PrettyModelForm(BootStrapModelForm):
    # # 验证规则
    # mobile = forms.CharField(
    #     # validators=[RegexValidator(r"^1[3-9]\d{9}$")],
    #     min_length=11,
    #     max_length=11,
    #     label="手机号"
    # )
    class Meta:
        model = PrettyNum
        fields = ('mobile','price','level','status')
        #fields="__all__"
        #exclude=['level']
        # widgets={
        #     "name":forms.TextInput(attrs={'class':'form-control'}),
        #     "password":forms.PasswordInput(attrs={'class':'form-control'}),
        #     "age":forms.TextInput(attrs={'class':'form-control'}),
        #     "account":forms.TextInput(attrs={'class':'form-control'}),
        #     "gender":forms.Select(attrs={'class':'form-control'}),
        #     "depart":forms.Select(attrs={'class':'form-control'}),
        # }
    # 方式2 钩子方法
    def clean_mobile(self):
        #当前编辑的那一行id
        # self.instance.pk
        txt_mobile = self.cleaned_data['mobile']
        # exists=PrettyNum.objects.exclude(self.instance.pk).filter(mobile=txt_mobile).exists()
        if self.instance.pk is not None:#解决编辑时的手机号问题
            exists = PrettyNum.objects.exclude(pk=self.instance.pk).filter(mobile=txt_mobile).exists()
        else:
            exists = PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("格式错误")
        # 验证通过
        return txt_mobile

class PrettyEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    # 验证：方式2
    def clean_mobile(self):
        # 当前编辑的哪一行的ID
        # print(self.instance.pk)
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile

class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets={
            # "detail":forms.Textarea(attrs={'class':'form-control'}),
        }

class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude=['oid','admin']


