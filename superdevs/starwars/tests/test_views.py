import pytest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse

from superdevs.starwars.models import Dataset
from superdevs.starwars.views import DatasetDetailView, DatasetDownloadRedirectView
from superdevs.users.models import User

pytestmark = pytest.mark.django_db


class TestDatasetDownload:
    def test_download_and_get_redirect_url(self, user: User, rf: RequestFactory, swapi_data_people, swapi_data_planet):
        view = DatasetDownloadRedirectView()
        view.planet_data = swapi_data_planet
        view.people_data = swapi_data_people
        request = rf.get("/starwars/download/")
        request.user = user
        view.request = request

        assert view.get_redirect_url() == "/starwars/"


class TestDatasetDetailView:
    def test_authenticated(self, swapi_data_context, user: User, dataset: Dataset, rf: RequestFactory):
        request = rf.get(f"/starwars/{dataset.pk}/")
        request.user = user
        # dataset = Dataset()
        DatasetDetailView.dataset = dataset
        DatasetDetailView.offline = True
        DatasetDetailView.offline_contex = swapi_data_context

        response = DatasetDetailView.as_view()(request, pk=dataset.pk)

        assert response.status_code == 200

    def test_not_authenticated(self, swapi_data_context, user: User, dataset: Dataset, rf: RequestFactory):
        request = rf.get(f"/starwars/{dataset.pk}/")
        request.user = AnonymousUser()
        DatasetDetailView.dataset = dataset
        DatasetDetailView.offline = True
        DatasetDetailView.offline_contex = swapi_data_context

        response = DatasetDetailView.as_view()(request, pk=dataset.pk)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/starwars/{dataset.pk}/"
