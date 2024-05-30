from io import BytesIO

from django.shortcuts import render, HttpResponse, redirect

from app01.models import Admin
from app01.utils.code import check_code
from app01.utils.form import LoginForm


def login(request):
    """登录"""
    if  request.method=="GET":
        form=LoginForm()
        context={
            'form':form
        }
        return render(request,'login.html',context=context)

    form = LoginForm(data=request.POST)
    context = {
        'form': form
    }
    if form.is_valid():
        #验证成功,获取到的用户名和密码
        #{'name': 'user', 'password': '123456'}
        # print(form.cleaned_data)
        #验证码的校验
        user_input_code=form.cleaned_data.pop('code')
        code=request.session.get('image_code',"")
        if code.upper()!=user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', context=context)


        #去数据库校验用户名和密码是否相同 获取用户对象、none
        admin_object=Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password","用户名或密码错误")
            return render(request, 'login.html', context=context)
        #用户名和密码输入正确
        #网站生成随机字符串；写到用户浏览器的cookie中，再写入到session中
        request.session["info"]={'id':admin_object.id,'name':admin_object.name}
        #session可以保存7天
        request.session.set_expiry(60*60*24*7)
        return redirect("/admin/list/")
    return render(request,'login.html',context=context)

def logout(request):
    """注销"""
    #将当前用户的session注销掉
    request.session.clear()
    return redirect("/login/")

def image_code(request):
    """生成图片验证码"""
    #调用pillow函数 生成图片
    img,code_string =check_code()
    print(code_string)

    #写入到自己的session中（以便于后续获取验证码  再进行校验）
    request.session["image_code"]=code_string
    #给session设置60s超时
    request.session.set_expiry(60)
    #写入内存文件中
    stream=BytesIO()
    img.save(stream,'png')
    stream.getvalue()
    return HttpResponse(stream.getvalue())
