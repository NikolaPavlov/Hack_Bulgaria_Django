import tempfile

from PIL import Image
from faker import Factory

from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Category, Offer
from .factories import CategoryFactory, OfferFactory, UserFactory

faker = Factory.create()


class IndexViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index_url')

    def test_open_index_return_200(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_index_page_return_only_approved_offers_with_status_2(self):
        OfferFactory.create(status=1)
        OfferFactory.create(status=2)
        OfferFactory.create(status=3)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.context['object_list'].count())


class PendingViewTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin',
                                                   'admin@mail.bg',
                                                   'admin')
        self.client = Client()
        self.url = reverse('pending_offers_url')

    def test_open_pending_page_return_200_with_admin_loged_in(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_403_if_try_to_open_pending_page_withowth_admin_loged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

    def test_pending_page_return_all_pending_offers_with_status_1(self):
        self.client.login(username='admin', password='admin')
        OfferFactory.create(status=1)
        OfferFactory.create(status=1)
        OfferFactory.create(status=1)
        OfferFactory.create(status=2)
        OfferFactory.create(status=3)

        response = self.client.get(self.url)
        self.assertEqual(3, response.context['object_list'].count())


class IndexViewByCategoriesFilterTests(TestCase):
    '''
    select specific category filter on index page
    should return the offers in the selected category
    '''
    def setUp(self):
        self.client = Client()

    def test_select_filter_for_categories_return_correct_offers_cat1(self):
        '''
        if category 1 is selected,
        only the offers in it with approved status 2
        should be apear on the screen
        '''
        category = CategoryFactory()
        OfferFactory.create_batch(3, category=category, status=2)
        # get 3 offers with status 2 approved in category1
        self.offer1_approved = Offer.objects.get(pk=1)
        self.offer2_approved = Offer.objects.get(pk=2)
        self.offer3_approved = Offer.objects.get(pk=3)

        response = self.client.get(reverse('offers_by_category_url',
                                           args=[category.id]))
        self.assertContains(response, Offer.objects.get(
            title=self.offer1_approved.title))
        self.assertContains(response, Offer.objects.get(
            title=self.offer2_approved.title))
        self.assertContains(response, Offer.objects.get(
            title=self.offer3_approved.title))

    def test_select_filter_for_categories_return_correct_offers_cat2(self):
        '''
        if category 2 is selected,
        only the offers in it with approved status 2
        should be apear on the screen
        '''
        category1 = CategoryFactory()
        category2 = CategoryFactory()
        OfferFactory.create_batch(3, category=category1, status=2)
        OfferFactory.create_batch(3, category=category1, status=1)
        OfferFactory.create_batch(3, category=category2, status=2)
        OfferFactory.create_batch(3, category=category2, status=1)
        offer_approved = Offer.objects.get(pk=7)

        response = self.client.get(reverse('offers_by_category_url',
                                           args=[category2.id]))
        self.assertContains(response, Offer.objects.get(
            title=offer_approved.title))


class LogInUserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='temp',
                                             email='temp@mail.bg',
                                             password='temp')
        self.url = reverse('login_url')

    def test_open_log_in_page_return_200(self):
        response = self.client.get(reverse('login_url'))
        self.assertEqual(200, response.status_code)

    def test_cant_login_with_wrong_username_and_pass(self):
        self.assertFalse(self.client.login(username=faker.word(),
                                           password=faker.word()))

    def test_can_log_in_with_correct_credentials(self):
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='temp'))


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
            'status': 1
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
            'image': tmp_file,
            'status': 1
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(302, response.status_code)
        self.assertEqual(1, Offer.objects.count())

    def test_cannot_create_offer_if_not_logged_in(self):
        image = Image.new('RGB', (100, 100), color='green')
        tmp_file = tempfile.NamedTemporaryFile(suffix='.png')
        image.save(tmp_file.name)

        data = {
            'title': faker.word(),
            'description': faker.text(),
            'price': 111,
            'category': self.category.id,
            'image': tmp_file,
            'status': 1
        }
        response = self.client.post(self.url, data)
        self.assertEqual(0, Offer.objects.count())
        self.assertEqual(302, response.status_code)

    def tearDown(self):
        self.client.logout()


class TestDetailView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='temp',
                                             email='temp@mail.bg',
                                             password='temp')
        self.url = reverse('offer_detail_url', args=(1, ))
        CategoryFactory.create_batch(3)
        self.category1 = Category.objects.get(pk=1)
        OfferFactory.create_batch(3, category=self.category1, author=self.user)

    def test_cannot_open_detail_page_for_offer_if_you_are_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(302, response.status_code)

    def test_can_open_detail_page_if_you_are_logged_in(self):
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='temp'))
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_in_detail_page_there_is_no_approve_button_for_normal_users(self):
        pass

    def test_in_detail_page_there_is_approve_button_for_admin(self):
        pass

    def test_superuser_can_approve_offer(self):
        pass

    def test_in_detail_page_there_is_no_reject_button_for_normal_users(self):
        pass

    def test_in_detail_page_there_is_reject_button_for_admin(self):
        pass

    def test_superuser_can_reject_offer(self):
        pass

    def test_edited_offer_move_to_pending_offers_for_approve_by_admin(self):
        pass


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

    def test_statistics_page_contains_the_names_of_categories_in_the_db(self):
        self.assertContains(self.response, Category.objects.get(pk=1).name)
        self.assertContains(self.response, Category.objects.get(pk=2).name)
        self.assertContains(self.response, Category.objects.get(pk=3).name)

    def test_statistics_page_contains_correct_num_of_offers_in_category(self):
        self.assertContains(self.response, self.category1.name)
        # 3 offers
        self.assertContains(self.response, 3)

    def test_check_user_statistics(self):
        self.assertContains(self.response, self.user.username)
        # 3 offers
        self.assertContains(self.response, 3)
        # 1 category
        self.assertContains(self.response, 1)

    def tearDown(self):
        self.client.logout()
