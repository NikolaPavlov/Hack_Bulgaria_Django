from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Offer


class BaseUserPassesTextMixin(UserPassesTestMixin):
    def test_func(self):
        return True


class CanUpdateOfferMixin(BaseUserPassesTextMixin):
    raise_exception = False

    def test_func(self):
        offer = get_object_or_404(Offer, pk=self.kwargs.get('pk'))

        if not offer.author == self.request.user:
            return False

        return True and super().test_func()


class IsSuperUserMixin(BaseUserPassesTextMixin):
    raise_exception = True

    def test_func(self):
        if not self.request.user.is_superuser:
            return False

        return True and super().test_func()

IsSuperUserMixin()
