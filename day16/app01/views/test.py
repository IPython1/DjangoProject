from django.shortcuts import render


def test(request):
    return  render(request,'layout_new.html')