import factory
from faker import Factory
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.hashers import make_password


faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.LazyAttribute(lambda _: faker.name())
    password = 'pass'
    email = factory.LazyAttribute(lambda _: faker.email())


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category
        django_get_or_create = ('name',)

    name = factory.LazyAttribute(lambda _: faker.word())


class OfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Offer

    title = factory.LazyAttribute(lambda _: faker.word())
    description = factory.LazyAttribute(lambda _: faker.text())
    price = 10
    # created_at
    category = factory.SubFactory(CategoryFactory)
    # image
    author = factory.SubFactory(UserFactory)
