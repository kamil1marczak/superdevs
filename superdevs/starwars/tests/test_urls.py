from django.urls import resolve, reverse

from superdevs.starwars.models import Dataset


def test_detail(dataset: Dataset):
    assert reverse("starwars:dataset", kwargs={"pk": dataset.pk}) == f"/starwars/dataset/{dataset.pk}/"
    assert resolve(f"/starwars/dataset/{dataset.pk}/").view_name == "starwars:dataset"


def test_download():
    assert reverse("starwars:download") == "/starwars/download/"
    assert resolve("/starwars/download/").view_name == "starwars:download"


def test_list():
    assert reverse("starwars:dataset_list") == "/starwars/"
    assert resolve("/starwars/").view_name == "starwars:dataset_list"
