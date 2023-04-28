import re

from superdevs.starwars.models import Dataset


def test_user_get_deleted_false(dataset: Dataset):
    assert dataset.is_deleted is False


def test_dataset_path(dataset: Dataset):
    assert re.match(r".*\.csv$", dataset.path)
