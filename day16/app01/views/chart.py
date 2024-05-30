from django.http import JsonResponse
from django.shortcuts import render, redirect

from app01.models import UserInfo, Department
from app01.utils.form import UserModelForm

def chart_list(request):
    """数据统计页面"""
    return render(request,'chart_list.html')
def chart_bar(request):
    """构造柱状图的数据"""
    legend=['杰杰','磊磊','鸡毛侯']
    series_list=[
        {
            'name':'杰杰',
            'type': 'bar',
            'data': [23, 24, 18, 25, 27, 28, 25]
        },
        {
            'name': '磊磊',
            'type': 'bar',
            'data': [26, 24, 18, 22, 23, 20, 27]
        },
        {
            'name': '鸡毛侯',
            'type': 'bar',
            'data': [30, 28, 28, 24, 29, 18, 25]
        }
    ]
    x_axis=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    result={
        'status':True,
        'data':{
            'legend':legend,
            'series_list':series_list,
            'x_axis':x_axis
        }
    }
    return JsonResponse(result)

def chart_line(request):
    """伪造折线图的数据"""
    legend = ['杰杰', '磊磊', '鸡毛侯']
    series_list = [
        {
            'name': '杰杰',
            'data': [23, 24, 18, 25, 27, 28, 25],
            'type': 'line'
        },
        {
            'name': '磊磊',
            'data': [26, 24, 18, 22, 23, 20, 27],
            'type': 'line'
        },
        {
            'name': '鸡毛侯',
            'data': [30, 28, 28, 24, 29, 18, 25],
            'type': 'line'
        }
    ]
    x_axis = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    result = {
        'status': True,
        'data': {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis
        }
    }
    return JsonResponse(result)

def chart_pie(request):
    """伪造饼图"""
    series_list=[
        {
            'value': 335,
            'name':'直接访问'
        },
        {
            'value':  234,
            'name':  '联盟广告'
        },
        {
            'value':  1548,
            'name': '搜索引擎'
        }
    ]
    result = {
        'status': True,
        'data': series_list,
    }
    return JsonResponse(result)

