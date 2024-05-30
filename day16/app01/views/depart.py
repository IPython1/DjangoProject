from django.shortcuts import render, redirect

from app01.models import Department
from app01.utils.pagination import Pagination


def depart_list(request):
    # UserInfo.objects.create(name="杰杰", password="123456", age=23)
    # UserInfo.objects.create(name="浩浩", password="123123", age=20)
    # UserInfo.objects.create(name="欣欣", password="123111", age=20)
    # UserInfo.objects.create(name="丽丽", password="123321", age=20)
    """部门列表"""
    #queryset 列表 [对象，对象，对象]
    queryset = Department.objects.all()
    page_object = Pagination(request, queryset, page_size=2)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html()
    }
    return render(request, 'depart_list.html',context=context)
def depart_add(request):
    if request.method == "GET":
        return render(request, "depart_add.html")
    # 获取用户提交的数据(title输入为空 怎么判断  后续用组件)
    title = request.POST.get("title")
    # 添加到数据库
    Department.objects.create(title=title)
    # 自动跳转
    # return redirect("http://127.0.0.1:8000/info/list/")
    return redirect("/depart/list/")
def depart_delete(request):
    if request.method == "GET":
        nid=request.GET.get("nid")
        Department.objects.filter(id=nid).delete()
        return redirect("/depart/list/")
def depart_edit(request,nid):
    #根据nid 更新数据
    # Department.objects.all().update(password="999")
    if request.method == "GET":
        row_object=Department.objects.filter(id=nid).first()
        print(row_object.id,row_object.title)
        return render(request, "depart_edit.html", {'row_object':row_object})
    # 获取用户提交的数据(title输入为空 怎么判断  后续用组件)
    title = request.POST.get("title")
    # 更新到数据库
    # Department.objects.all().update(title=title)
    Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")