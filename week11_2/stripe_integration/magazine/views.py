from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Magazine, Article
from stripe_integration.settings import STRIPE_API_KEY, STRIPE_PUBLIC_KEY
import stripe


class MagazineListview(LoginRequiredMixin, ListView):
    model = Magazine
    template_name = 'magazine/list.html'

    stripe.setPublishableKey(STRIPE_PUBLIC_KEY)

    # def get_context_data(*args, **kwargs):
    #     super().get_context_data()


class ArticleListview(ListView):
    model = Article
    template_name = 'magazine/article_list.html'

    def get_queryset(self):
        return self.model.objects\
                         .filter(magazine_id=self.kwargs.get('magazine_id'))
