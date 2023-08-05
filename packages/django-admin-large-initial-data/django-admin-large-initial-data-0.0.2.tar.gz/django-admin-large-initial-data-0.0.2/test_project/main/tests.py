from . import models

from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import Client, TestCase, RequestFactory

from large_initial import build_redirect_url


class LargeInitialTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.client.force_login(
            User.objects.create(is_superuser=True, is_staff=True),
        )

    def test_build_no_params(self):
        request = self.factory.get("")
        middleware = SessionMiddleware()
        middleware.process_request(request)
        address = build_redirect_url(
            request,
            'admin:main_album_add',
        )
        self.assertEquals(
            address,
            "/admin/main/album/add/"
        )

    def test_build_bad_field(self):
        address = "/admin/main/album/add?asdf=asdf"
        response = self.client.get(address, follow=True)
        self.assertContains(
            response,
            '<h1>Add album</h1>',
            html=True,
        )

    def test_build_large(self):
        request = self.factory.get("")
        middleware = SessionMiddleware()
        middleware.process_request(request)
        musicians = [
            models.Musician.objects.create(name="model {}".format(i))
            for i in range(0, 2000)
        ]
        address = build_redirect_url(
            request,
            'admin:main_album_add',
            params={'artists': musicians},
        )
        self.assertEquals(
            address,
            "/admin/main/album/add/?"
            "artists=session-109fd1dcec14f5b08e0edc9de1560a53",
        )
        self.assertEquals(
            request.session.get('session-109fd1dcec14f5b08e0edc9de1560a53'),
            ",".join([str(i) for i in range(1, 2001)]),
        )

        session = self.client.session
        session['documents_to_share_ids'] = [1]
        session['session-109fd1dcec14f5b08e0edc9de1560a53'] = \
            request.session.get('session-109fd1dcec14f5b08e0edc9de1560a53')
        session.save()
        response = self.client.get(address, follow=True)
        self.assertContains(
            response,
            '<option value="2000" selected="selected">Musician object</option>',
            html=True,
        )

    def test_build_small(self):
        request = self.factory.get("")
        middleware = SessionMiddleware()
        middleware.process_request(request)
        musicians = [
            models.Musician.objects.create(name="model {}".format(i))
            for i in range(0, 2)
        ]
        address = build_redirect_url(
            request,
            'admin:main_album_add',
            params={'artists': musicians},
        )
        self.assertEquals(
            address,
            "/admin/main/album/add/?artists=1%2C2",
        )

        response = self.client.get(address, follow=True)
        self.assertContains(
            response,
            '<option value="2" selected="selected">Musician object</option>',
            html=True,
        )
