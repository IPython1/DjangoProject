from django.shortcuts import render, HttpResponse, redirect

from app01.models import UserInfo


def orm(request):
    # Department.objects.create(title="销售部")
    # Department.objects.create(title="运营部")
    UserInfo.objects.create("浩浩","123",23,100.68,"2024-05-21",1,4)
    UserInfo.objects.create("杰杰", "123", 23, 100.68, "2024-05-21", 1, 1)
    UserInfo.objects.create("磊磊", "123", 23, 100.68, "2024-05-21", 1, 4)
    UserInfo.objects.create("帆帆", "123", 23, 100.68, "2024-05-21", 1, 1)
    return HttpResponse("添加成功")