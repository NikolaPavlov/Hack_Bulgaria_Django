import math

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# Create your views here.
def sum(request, a, b):
    result = int(a) + int(b)
    if request.GET.get('format') == 'json':
        # import ipdb;ipdb.set_trace()
        return JsonResponse({'result': result})
    else:
        return HttpResponse(result)


def multiply(request, a, b):
    result = int(a) * int(b)
    if request.GET.get('format') =='json':
        return JsonResponse({'result': result})
    else:
        return HttpResponse(result)


def power(request, a, b):
    result = math.pow(int(a), int(b))
    result = int(result)
    if request.GET.get('format') =='json':
        return JsonResponse({'result': result})
    else:
        return HttpResponse(result)


def fact(request, a):
    result = math.factorial(int(a))
    if request.GET.get('format') =='json':
        return JsonResponse({'result': result})
    else:
        return HttpResponse(result)
