from factory import Faker
from factory.django import DjangoModelFactory

from superdevs.starwars.models import Dataset


class DatasetFactory(DjangoModelFactory):
    path = Faker("file_path", depth=2, extension="csv")

    class Meta:
        model = Dataset
        django_get_or_create = [
            "path",
        ]
