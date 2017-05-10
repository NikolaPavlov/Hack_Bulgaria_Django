from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from .models import Category, Offer
from .forms import LoginForm, AddOfferForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count


# Create your views here.
def index(request):
    all_categories = Category.objects.all()
    try:
        select_category_id = request.GET['category_id']
        selected_category = Category.objects.filter(id=select_category_id)
        selected_offers = Offer.objects.filter(category=selected_category)
        return render(request, 'hack_olx/index.html', locals())
    except:
        selected_offers = Offer.objects.all()
    return render(request, 'hack_olx/index.html', locals())


def register(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user, created = User.objects.get_or_create(username=form.cleaned_data['username'])
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.save()
        return redirect(reverse(login_view))

    return render(request, 'hack_olx/register.html', locals())


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            # user = authenticate(**form.cleaned_data)
        if user is not None:
            login(request, user)
            return redirect(reverse(index))
        if user is None:
            form.add_error(field='', error='No such user! Try again mf!')

    return render(request, 'hack_olx/login.html', locals())


@login_required(login_url=reverse_lazy('login_url'))
def logout_view(request):
    logout(request)
    return redirect(reverse(index))


@login_required(login_url=reverse_lazy('login_url'))
def add_offer(request):
    form = AddOfferForm()
    if request.method == 'POST':
        form = AddOfferForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            f.save()
            return redirect(reverse(index))
    return render(request, 'hack_olx/add_offer.html', locals())


def statistics(request):
    # return top categories
    top3_categories = Category.objects.annotate(num_offers=Count('offer')).order_by('-num_offers')[:3]
    top3_users = Offer.objects.values("author__username").annotate(number_of_offers=Count('author__id')).annotate(number_of_categories=Count('category__id', distinct=True)).order_by('-number_of_offers')[:3]
    return render(request, 'hack_olx/statistics.html', locals())
