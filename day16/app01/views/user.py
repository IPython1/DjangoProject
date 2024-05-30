#用户管理
from django.shortcuts import render, redirect

from app01.models import UserInfo, Department
from app01.utils.form import UserModelForm
from app01.utils.pagination import Pagination


def user_list(request):
    """用户列表"""
    #queryset 列表 [对象，对象，对象]
    queryset = UserInfo.objects.all()
    #obj.depart_id 获取数据库中存储的那个字段值
    #xx=Department.objects.filter(id=obj.depart_id).first()
    #xx.title
    #obj.depart.  根据id自动去关联的表中获取那一行数据的depart对象
    page_object = Pagination(request, queryset,page_size=5)
    context = {
        'queryset':page_object.page_queryset,
        'page_string':page_object.html()
    }
    return render(request, 'user_list.html',context=context)
def user_add(request):
    """添加用户"""
    if request.method == "GET":
        context={
            'gender_choices':UserInfo.gender_choices,
            'depart_list':Department.objects.all(),
        }
        return render(request, "user_add.html",context=context)
    # #获取用户提交的数据
    # user = request.POST.get("title")
    # # 添加到数据库
    # UserInfo.objects.create(title=title)
    # 自动跳转
    # return redirect("http://127.0.0.1:8000/info/list/")
    return redirect("/depart/list/")

def user_model_form_add(request):
    """添加用户 modelform版本"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_model_form_add.html", {'form':form})
    # #获取用户提交的数据
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # print(form.cleaned_data)
        # # 添加到数据库
        # UserInfo.objects.create(title=title)
        form.save()

        # 自动跳转
        # return redirect("http://127.0.0.1:8000/info/list/")
        return redirect("/user/list/")
    else:# 校验失败 页面上显示错误信息
        return render(request, "user_model_form_add.html", {'form':form})
def user_edit(request,nid):
    """编辑用户"""
    row_object = UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        #根据id去数据库获取要编辑的那一行数据
        form=UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {'form':form})

    form=UserModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        #默认保存的是用户输入的所有数据，如果想要在用户输入以外增加一点值
        #form.instance.字段名=值
        form.save()
        return redirect("/user/list/")
    return render(request, "user_edit.html", {'form':form})
def user_delete(request,nid):
    """删除用户"""
    if request.method == "GET":
        UserInfo.objects.get(id=nid).delete()
        return redirect("/user/list/")