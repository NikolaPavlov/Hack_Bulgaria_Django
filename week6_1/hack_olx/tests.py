from django.test import TestCase, Client
from django.urls import reverse
from .factories import UserFactory, CategoryFactory, OfferFactory
from django.contrib.auth.models import User
from .models import Offer, Category
from PIL import Image
import tempfile

from faker import Factory


faker = Factory.create()


class IndexViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index_url')

    def test_open_index_return_200(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_list_n_offers_in_index_page(self):
        self.offer = OfferFactory.create_batch(9)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(9, response.context['selected_offers'].count())


class IndexViewByCategoriesFilterTests(TestCase):
    '''
    select specific category filter on index page
    should return the offers in the selected category
    '''
    def setUp(self):
        self.client = Client()
        self.url = reverse('index_url')
        self.categories = CategoryFactory.create_batch(9)
        self.category1 = Category.objects.get(pk=1)
        self.category2 = Category.objects.get(pk=2)
        OfferFactory.create_batch(3, category=self.category1)
        OfferFactory.create_batch(3, category=self.category2)

    def test_select_filter_for_categories_return_correct_offers_cat1(self):
        '''
        if category 1 is selected,
        only the offers in it should be apear on the screen
        '''
        response = self.client.get(self.url, {'category_id': 1})
        self.assertContains(response, Offer.objects.get(pk=1).title)
        self.assertContains(response, Offer.objects.get(pk=2).title)
        self.assertContains(response, Offer.objects.get(pk=3).title)

    def test_select_filter_for_categories_return_correct_offers_cat2(self):
        '''
        if category 1 is selected,
        only the offers in it should be apear on the screen
        '''
        response = self.client.get(self.url, {'category_id': 2})
        self.assertContains(response, Offer.objects.get(pk=4).title)
        self.assertContains(response, Offer.objects.get(pk=5).title)
        self.assertContains(response, Offer.objects.get(pk=6).title)


class LogInUserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
                username='temp',
                email='temp@mail.bg',
                password='temp')
        self.url = reverse('login_url')

    def test_open_log_in_page_return_200(self):
        response = self.client.get(reverse('login_url'))
        self.assertEqual(200, response.status_code)

    def test_cant_login_with_wrong_username_and_pass(self):
        self.assertFalse(self.client.login(username=faker.word(), password=faker.word()))

    def test_can_log_in_with_correct_credentials(self):
        self.assertTrue(self.client.login(username=self.user.username, password='temp'))


class CreateOffer(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('add_offer_url')
        self.category = CategoryFactory()
        self.user = User.objects.create_user(
            username='temp',
            email='temp@mail.bg',
            password='temp')

    def test_redirect_to_login_page_if_user_is_not_logged_and_open_add_offer(self):
        response = self.client.get(reverse('add_offer_url'))
        self.assertEqual(302, response.status_code)

    def test_cannot_create_offer_withowth_select_category(self):
        self.client.login(username=self.user.username, password='temp')
        data = {
            'title': faker.word(),
            'description': faker.text(),
            'price': faker.numerify(),
        }
        response = self.client.post(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, Offer.objects.count())

    def test_cannot_create_offer_withowth_title(self):
        self.client.login(username=self.user.username, password='temp')
        data = {
            'description': faker.text(),
            'price': faker.numerify(),
            'category': self.category.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, Offer.objects.count())

    def test_cannot_create_offer_withowth_price(self):
        self.assertEqual(0, Offer.objects.count())
        self.client.login(username=self.user.username, password='temp')
        data = {
            'title': faker.word(),
            'description': faker.text(),
            'category': self.category.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, Offer.objects.count())

    def test_cannot_create_offer_withoth_description(self):
        self.assertEqual(0, Offer.objects.count())
        self.client.login(username=self.user.username, password='temp')
        data = {
            'title': faker.word(),
            'price': faker.numerify(),
            'category': self.category.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, Offer.objects.count())

    def test_crete_offer_success_withowth_img(self):
        self.client.login(username=self.user.username, password='temp')
        self.assertEqual(0, Offer.objects.count())

        image = Image.new('RGB', (100, 100), color='green')
        tmp_file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(tmp_file.name)

        data = {
            'title': faker.word(),
            'description': faker.text(),
            'price': 111,
            'category': self.category.id,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(302, response.status_code)
        self.assertEqual(1, Offer.objects.count())

    def test_crete_offer_with_correct_input_data(self):
        self.client.login(username=self.user.username, password='temp')
        self.assertEqual(0, Offer.objects.count())

        image = Image.new('RGB', (100, 100), color='green')
        tmp_file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(tmp_file.name)

        data = {
            'title': faker.word(),
            'description': faker.text(),
            'price': 111,
            'category': self.category.id,
            'image': tmp_file
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(302, response.status_code)
        self.assertEqual(1, Offer.objects.count())

    def tearDown(self):
        self.client.logout()


class TestStatisticsPage(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.url = reverse('statistics_url')
        CategoryFactory.create_batch(3)
        self.category1 = Category.objects.get(pk=1)
        OfferFactory.create_batch(3, category=self.category1, author=self.user)
        self.response = self.client.get(self.url)

    def test_statistics_page_can_be_viewed_by_unregister_unlogged_user(self):
        self.assertEqual(200, self.response.status_code)
    #
    def test_statistics_page_contains_the_names_of_categories_in_the_db(self):
        self.assertContains(self.response, Category.objects.get(pk=1).name)
        self.assertContains(self.response, Category.objects.get(pk=2).name)
        self.assertContains(self.response, Category.objects.get(pk=3).name)

    def test_statistics_page_contains_exact_representation_str_for_offers_in_specific_category(self):
        '''
        check if
            {{ self.cattegory1.name }} - 3offers
        string is in the response of statistics page
        '''
        correct_representation_str = self.category1.name + ' - 3'
        self.assertContains(self.response, correct_representation_str)

    def test_check_user_statistics(self):
        '''
        check if
            {{ self.user.username }}-3offers-1categories
        string is in the response of statistics page
        '''
        correct_representation_str = self.user.username + '-' + '3offers' + '-' + '1categories'
        self.assertContains(self.response, correct_representation_str)

    def tearDown(self):
        self.client.logout()
