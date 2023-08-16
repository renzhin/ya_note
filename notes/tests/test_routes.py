# notes/tests/test_routes.py
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author1 = User.objects.create(username='Лев Толстой')
        cls.author2 = User.objects.create(username='Анна Петрова')
        cls.notes1 = Note.objects.create(
            title='1',
            text='Текст2',
            author=cls.author1,
        )
        cls.notes2 = Note.objects.create(
            title='Zagolovok1',
            text='Текст2',
            author=cls.author2,
        )

    def test_pages_availability(self):
        urls = (
            ('notes:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_notes_view(self):
        users_statuses = (
            (self.author1, HTTPStatus.OK),
            (self.author2, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            # Логиним пользователя в клиенте:
            self.client.force_login(user)
            # Для каждой пары "пользователь - ожидаемый ответ"
            # перебираем имена тестируемых страниц:
            for name in ('notes:detail', 'notes:detail'):
                with self.subTest(user=user, name=name):

                    url = reverse(name, args=self.notes1.slug,)
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)