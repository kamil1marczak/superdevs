import os

from django.core.exceptions import ValidationError

from superdevs.starwars.models import Dataset


def _validate_file_name_unique_DB(file_path):
    if Dataset.objects.filter(path=file_path).exists():
        raise ValidationError("Dataset with this name already exists")


def _validate_file_name_unique_os(file_path):
    if os.path.isfile(file_path):
        raise ValidationError("File with this name already exists")
