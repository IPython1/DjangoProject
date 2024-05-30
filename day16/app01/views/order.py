from datetime import datetime
from random import randint, random

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01.models import Order
from django.shortcuts import render,HttpResponse

from app01.utils.form import OrderModelForm
from app01.utils.pagination import Pagination


def order_list(request):
    queryset = Order.objects.all().order_by('-id')
    form=OrderModelForm()
    page_object = Pagination(request, queryset)
    context={
        'form':form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码

    }
    return render(request,'order_list.html',context=context)

@csrf_exempt
def order_add(request):
    """新建订单 Ajax请求"""
    form=OrderModelForm(data=request.POST)
    if form.is_valid():
        #额外增加一些不是用户输入的值（自己计算出来） 订单号
        form.instance.oid = datetime.now().strftime('%Y%m%d%H%M%S')+str(randint(1000,9999))
        #固定设置管理员ID 从登录信息的session中获取
        form.instance.admin_id=request.session['info']['id']
        #保存到数据库中
        form.save()
        return JsonResponse({'status': True})
        # return HttpResponse(json.dumps({'status': True}))
    return JsonResponse({'status': False,'error':form.errors})

def order_delete(request):
    uid=request.GET.get('uid')
    exists = Order.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status': False,'error':'数据不存在'})
    Order.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})

def order_detail(request):
    """根据id获取订单详细"""
    #想去数据库获取数据时：对象/字典/元组[(1,'xx'),(2,'xxx')]
    uid = request.GET.get('uid')
    row_dict = Order.objects.filter(id=uid).values('title','price','status').first()
    print(row_dict)
    if not row_dict:
        return JsonResponse({'status': False, 'error': '数据不存在'})
    # result={
    #     'status':True,
    #     'data':row_dict
    # }
    return JsonResponse({'status': True, 'data': row_dict})
    '''方式一
    uid = request.GET.get('uid')
    row_object=Order.objects.filter(id=uid).first()

    if not row_object:
        return JsonResponse({'status': False, 'error': '数据不存在'})
    #从数据库中获取到一个对象 row_object
    result={
        'status': True,
        'data':{
            'title':row_object.title,
            'price':row_object.price,
            'status':row_object.status,
        }
    }
    return JsonResponse(result)
    '''

@csrf_exempt
def order_edit(request):
    """编辑订单"""
    uid=request.GET.get('uid')
    row_object=Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({'status': False, 'tips': '数据不存在,请刷新重试'})
    form=OrderModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})




