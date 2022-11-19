from http import HTTPStatus

from django.test import TestCase, Client
from django.urls import reverse

from authapp.models import User
from mainapp.models import News


class StaticPageSmokeTest(TestCase):

    def test_page_index_open(self):
        url = reverse('mainapp:index')
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_contacts_open(self):
        url = reverse('mainapp:contacts')
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)


class NewsTestCase(TestCase):

    def setUp(self) -> None:
        super().setUp()
        for i in range(10):
            News.objects.create(
                title=f'title {i}',
                preamble=f'preamble {i}',
                body=f'body {i}'
            )
        User.objects.create_superuser(username='user', password='user')
        self.client_with_auth = Client()
        auth_url = reverse('authapp:login')
        self.client_with_auth.post(
            auth_url,
            {'username': 'user', 'password': 'user'}
        )

    def test_open_page(self):
        url = reverse('mainapp:news')
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_failed_open_add_by_anonim(self):
        url = reverse('mainapp:news_create')
        result = self.client.get(url)
        self.assertEqual(result.status_code, HTTPStatus.FOUND)

    def test_create_news_tem_by_admin(self):
        news_count = News.objects.count()
        url = reverse('mainapp:news_create')
        result = self.client_with_auth.post(
            url,
            data={
                'title': 'title',
                'preamble': 'preamble',
                'body': 'body'
            }
        )

        self.assertEqual(result.status_code, HTTPStatus.OK)
        self.assertEqual(News.objects.count(), news_count + 1)
