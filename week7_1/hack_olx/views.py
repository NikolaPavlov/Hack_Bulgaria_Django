import django

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.forms.models import model_to_dict
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from .forms import AddOfferForm, LoginForm, UserRegisterForm
from .mixins import CanUpdateOfferMixin, IsSuperUserMixin
from .models import Category, Offer

# Create your views here.
class OffersIndexView(ListView):
    '''
    return all offers with status 2 (approved status code)
    '''
    model = Offer
    template_name = 'hack_olx/index.html'
    queryset = Offer.objects.select_related('category', 'author').filter(status=2)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all()
        return context


class ApprovedAndRejectedOffes(LoginRequiredMixin, ListView):
    '''
    approved and rejected offers for the current user
    '''
    model = Offer
    template_name = 'hack_olx/index.html'
    context_object_name = 'offers'

    def get_queryset(self):
        return Offer.objects.filter(author=self.request.user, status__in=[2, 3])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class OfferDetailView(LoginRequiredMixin, DetailView):
    model = Offer
    template_name = 'hack_olx/offer_details.html'
    login_url = reverse_lazy('login_url')


class UpdateOfferView(LoginRequiredMixin, CanUpdateOfferMixin, UpdateView):
    '''
    user can update his own posts
    '''
    model = Offer
    form_class = AddOfferForm
    template_name = 'hack_olx/add_offer.html'
    login_url = reverse_lazy('login_url')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 1
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index_url')


class DeleteOfferView(LoginRequiredMixin, CanUpdateOfferMixin, DeleteView):
    '''
    user can delete his own posts
    '''
    model = Offer
    success_url = reverse_lazy('index_url')
    login_url = reverse_lazy('login_url')


class OfferPendingListView(LoginRequiredMixin, IsSuperUserMixin, ListView):
    '''
    return all offers with status 1 pending if user is admin
    '''
    model = Offer
    template_name = 'hack_olx/index.html'
    queryset = Offer.objects.select_related('category', 'author').filter(status=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all()
        return context


# TODO: admin user approve and regect offers in pending view
@login_required
@staff_member_required
def offer_approve(request, pk):
    offer = Offer.objects.get(pk=pk)
    offer.status = 2
    offer.save()
    return redirect(reverse('index_url'))


@login_required
@staff_member_required
def offer_reject(request, pk):
    offer = Offer.objects.get(pk=pk)
    offer.status = 3
    offer.save()
    return redirect(reverse('index_url'))


class OffersByCategoryView(ListView):
    model = Offer
    template_name = 'hack_olx/index.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Offer.objects.filter(category=self.category, status=2)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all()
        # context['current_category'] = get_object_or_404(Category,
        #                                                 pk=self.kwargs['pk'])
        context['current_category'] = self.category
        return context


class OfferCreateView(LoginRequiredMixin, CreateView):
    model = Offer
    template_name = 'hack_olx/add_offer.html'
    form_class = AddOfferForm
    login_url = reverse_lazy('login_url')

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super(OfferCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index_url')


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
        if user is not None:
            login(request, user)
            return redirect(reverse('index_url'))
        if user is None:
            form.add_error(field='', error='No such user! Try again mf!')

    return render(request, 'hack_olx/login.html', locals())


def logout_view(request):
    logout(request)
    return redirect(reverse('index_url'))
