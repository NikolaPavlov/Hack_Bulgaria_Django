from django.test import TestCase, Client
from blog.factories import BlogPostFactory, TagFactory
from blog.models import BlogPost


class CustomQuerySetTests(TestCase):
    def setUp(self):
        self.blog_post = BlogPostFactory()
        self.private_blog_post = BlogPostFactory(is_private=True)

    def test_get_private_post_from_obj_manager(self):
        private_posts = BlogPost.objects.get_private_posts()
        self.assertIn(self.private_blog_post, private_posts)
