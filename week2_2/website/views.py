from django.shortcuts import render, get_object_or_404, redirect
from api.models import User, Data


# Create your views here.
def index(request):
    '''
        Return:
            total num of users
            total num of keys
            histogram of all keys
        Generate table with all users as links to user details
    '''
    all_users = User.objects.all()
    all_users_count = all_users.count()
    all_data = Data.objects.all()
    all_data_count = all_data.count()
    histogram = {}

    for d in all_data:
        if d.key not in histogram:
            histogram[d.key] = 1
        else:
            histogram[d.key] += 1
    return render(request, 'index.html', locals())


def detail_view(request, identifier):
    '''
        Return:
            users key value as table
    '''
    u = get_object_or_404(User, identifier=identifier)
    all_data = u.data_set.all()
    context = {'all_data': all_data, 'identifier': identifier}
    return render(request, 'detail.html', context)


def add_key(request, identifier):
    '''
        Write:
            user key value values for user with given identifier
    '''
    if request.method == "POST":
        u = get_object_or_404(User, identifier=identifier)
        key = request.POST['key']
        value = request.POST['value']
        try:
            d = Data.objects.get(key=key, user=u)
            d.delete()
            Data.objects.create(key=key, value=value, user=u)
        except Data.DoesNotExist:
            Data.objects.create(key=key, value=value, user=u)
        return redirect('detail_view', identifier=identifier)
    elif request.method == "GET":
        return render(request, 'add_key.html', {})
