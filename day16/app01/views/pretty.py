from django.shortcuts import render, redirect

from app01.models import PrettyNum
from app01.utils.form import PrettyModelForm
from app01.utils.pagination import Pagination


def pretty_list(request):
    """靓号列表 实现模糊查询"""
    data_dict={}
    search_data=request.GET.get("q","")
    if search_data is not None:
        data_dict["mobile__contains"]=search_data

    queryset=PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object=Pagination(request,queryset)
    page_queryset=page_object.page_queryset
    page_string=page_object.html()
    context={
        "search_data": search_data,

        "queryset":page_queryset,#分完页的数据
        "page_string":page_string,#页码

    }
    # [page_object.start:page_object.end]
    return render(request,"pretty_list.html",context=context)
def pretty_add(request):
    """添加用户 modelform版本"""
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {'form':form})
    # #获取用户提交的数据
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # print(form.cleaned_data)
        #{'name':'admin','password':'123',confirm_password:'456'}
        # # 添加到数据库
        # UserInfo.objects.create(title=title)
        form.save()

        # 自动跳转
        # return redirect("http://127.0.0.1:8000/info/list/")
        return redirect("/pretty/list/")
    else:# 校验失败 页面上显示错误信息
        return render(request, "pretty_add.html", {'form':form})
def pretty_edit(request,nid):
    """编辑靓号"""
    row_object = PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据id去数据库获取要编辑的那一行数据
        form = PrettyModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {'form': form})

    form = PrettyModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要在用户输入以外增加一点值
        # form.instance.字段名=值
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_edit.html", {'form': form})
def pretty_delete(request,nid):
    """删除靓号"""
    if request.method == "GET":
        PrettyNum.objects.get(id=nid).delete()
        return redirect("/pretty/list/")