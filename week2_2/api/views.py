from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from .models import User, Data
import uuid
import json


# Create your views here.
def create_user_view(request):
    identifier = uuid.uuid4()
    User.objects.create(identifier=identifier)
    payload = {"identifier": identifier}
    return JsonResponse(payload, status=200)


def set_key_view(request, identifier):
    # recive {"key": key, "value": value} json
    '''
        Parse the json and put it in Data model
        raise 404 if identifier not lead to User
    '''
    u = get_object_or_404(User, identifier=identifier)
    data = json.loads(request.body)
    key = data['key']
    value = data['value']
    # Data.objects.create(key=key, value=value, user=u)
    try:
        Data.objects.get(key=key, user=u)
        d1 = Data.objects.get(key=key, user=u)
        d1.delete()
    except Data.DoesNotExist:
        pass
    d = Data(key=key, value=value, user=u)
    d.save()
    return JsonResponse({'key': key, "value": value}, status=201)


def manage_key_view(request, identifier, key):
    if request.method == "GET":
        u = User.objects.get(identifier=identifier)
        try:
            d = Data.objects.get(key=key, user=u)
            payload = {'key': d.key, "value": d.value}
            return JsonResponse(payload, status=200)
        except:
            return JsonResponse({"error": "Key not found"}, status=404)
    if request.method == "DELETE":
        try:
            u = User.objects.get(identifier=identifier)
        except User.DoesNotExist:
            return JsonResponse({}, status=404)
        try:
            d = Data.objects.get(key=key, user=u)
        except Data.DoesNotExist:
            return JsonResponse({}, status=404)
        d.delete()
        return JsonResponse({}, status=202)
