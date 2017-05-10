from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Offer
from .forms import LoginForm, AddOfferForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.generic import (ListView,
                                  CreateView,
                                  DetailView,
                                  TemplateView,
                                  UpdateView)

from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class OfferListView(ListView):
    model = Offer
    template_name = 'hack_olx/offer_list.html'

    def get_queryset(self):
        return Offer.objects.select_related('category', 'author').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all()
        return context


class OffersByCategoryView(ListView):
    model = Offer
    template_name = 'hack_olx/offers_by_category.html'

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Offer.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs['pk'])
        return context


class OfferCreateView(LoginRequiredMixin, CreateView):
    model = Offer
    template_name = 'hack_olx/add_offer.html'
    form_class = AddOfferForm

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super(OfferCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index_url')


class OfferDetailView(LoginRequiredMixin, DetailView):
    model = Offer
    template_name = 'hack_olx/offer_details.html'
    context_object_name = 'offer'

    def get_object(self):
        return get_object_or_404(Offer, pk=self.kwargs['pk'])


class StatisticTemplateView(TemplateView):
    template_name = 'hack_olx/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['top3_categories'] = Category.objects.annotate(
            num_offers=Count('offer')).order_by('-num_offers')[:3]

        context['top3_users'] = Offer.objects.values(
            "author__username").annotate(number_of_offers=Count(
                'author__id')).annotate(number_of_categories=Count(
                    'category__id', distinct=True)).order_by('-number_of_offers')[:3]
        return context


class UpdateOfferView(LoginRequiredMixin, UpdateView):
    model = Offer
    form_class = AddOfferForm
    template_name = 'hack_olx/add_offer.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index_url')


# TODO: change login system to class based
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
            return redirect(reverse('index_url'))
        if user is None:
            form.add_error(field='', error='No such user! Try again mf!')

    return render(request, 'hack_olx/login.html', locals())


@login_required(login_url=reverse_lazy('login_url'))
def logout_view(request):
    logout(request)
    return redirect(reverse('index_url'))
