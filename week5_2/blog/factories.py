import factory
from faker import Factory
from factory.django import DjangoModelFactory
from .models import Tag, BlogPost


faker = Factory.create()


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    tag_name = factory.LazyAttribute(lambda _: faker.word())


class BlogPostFactory(DjangoModelFactory):
    class Meta:
        model = BlogPost

    title = factory.LazyAttribute(lambda _: faker.word())
    content = factory.LazyAttribute(lambda _: faker.text())
    created_at = faker.date_time()
    updated_at = faker.date_time()

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.tags.add(group)

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.authors.add(group)
