import json

from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app01.models import Task
from app01.utils.form import TaskModelForm
from app01.utils.pagination import Pagination


def task_list(request):
    """任务列表"""
    #去数据库获取所有的任务
    queryset=Task.objects.all()
    page_object = Pagination(request, queryset)
    # for obj in queryset:
    #     print(obj.get_level_display())
    form=TaskModelForm()
    context={
        'form':form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'task_list.html',context=context)

#免除csrf表单认证
@csrf_exempt
def task_ajax(request):
    # print(request.GET)
    print(request.POST)
    #
    data_dict={"status": True,'data':[11,22,33,44]}
    # json_string = json.dumps(data_dict)
    # return HttpResponse(json_string)
    return JsonResponse(data_dict)
@csrf_exempt
def task_add(request):
    #通过ajax方式将数据发过来
    print(request.POST)

    #1.用户发送过来的数据进行校验（Modelform进行校验）
    form=TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return JsonResponse(data_dict)
    data_dict = {"status": False,'error':form.errors}
    return JsonResponse(data_dict)
