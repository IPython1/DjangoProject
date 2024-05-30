from django.shortcuts import render, redirect

from app01.models import Admin
from app01.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm
from app01.utils.pagination import Pagination

def admin_list(request):
    """管理员列表"""
    #中间件判断是否有cookie信息
    #搜索功能 构造搜索条件
    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data is not None:
        data_dict["name__contains"] = search_data
    #根据搜索条件去数据库获取
    queryset=Admin.objects.filter(**data_dict)

    #分页
    page_object=Pagination(request,queryset,)
    context={
        'queryset':page_object.page_queryset,
        'page_string':page_object.html(),
        'search_data':search_data,
    }
    return render(request,'admin_list.html',context=context)

def admin_add(request):
    """添加管理员"""
    title='新建管理员'
    if request.method == "GET":
        form = AdminModelForm()
        return render(request,'change.html',{"title":title,'form':form})
    # #获取用户提交的数据
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # print(form.cleaned_data)
        # # 添加到数据库
        # UserInfo.objects.create(title=title)
        form.save()
        # 自动跳转
        # return redirect("http://127.0.0.1:8000/info/list/")
        return redirect("/admin/list/")
    else:  # 校验失败 页面上显示错误信息
        return render(request, "change.html", {"title":title,'form': form})

def admin_edit(request,nid):
    """编辑管理员"""
    #对象/none
    row_object=Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request,'error.html',{'msg':'数据不存在'})

    title='编辑管理员'
    if request.method == "GET":
        #编辑的时候显示默认值 instance=row_object
        form=AdminEditModelForm(instance=row_object)
        context = {
            'title':title,
            'form':form,
        }
        return render(request,'change.html',context=context)

    form=AdminEditModelForm(data=request.POST,instance=row_object)
    context = {
        'title': title,
        'form': form,
    }
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, 'change.html', context=context)

def admin_delete(request,nid):
    """删除靓号"""
    if request.method == "GET":
        Admin.objects.get(id=nid).delete()
        return redirect("/admin/list/")

def admin_reset(request,nid):
    """重置密码"""
    # 对象/none
    row_object = Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '数据不存在'})

    title = '重置密码 - {}'.format(row_object.name)
    if request.method == "GET":
        # 编辑的时候显示默认值 instance=row_object
        form = AdminResetModelForm()
        context = {
            'title': title,
            'form': form,
        }
        return render(request, 'change.html', context=context)

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    context = {
        'title': title,
        'form': form,
    }
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, 'change.html', context=context)

