import json
import logging
import os
import uuid
from typing import Literal

import clients
import petl as etl
from django.conf import settings

from superdevs.common.exceptions import ApplicationError
from superdevs.common.services import model_update
from superdevs.starwars.models import Dataset
from superdevs.starwars.validators import _validate_file_name_unique_DB, _validate_file_name_unique_os

logger = logging.getLogger(__name__)

DATA_CATEGORIES = Literal["people", "planets", "films", "species", "vehicles", "starships"]


def get_all_results(url: DATA_CATEGORIES) -> list[dict | None]:
    """
    Fetch all results from a SWAPI endpoint.

    This method uses clients library to connect to SWAPI and fetch all results base on given category of data

    Args:
        url (DATA_CATEGORIES): Category of data to fetch from SWAPI
    Returns:
        List[Optional[dict]]: List constructed from SWAPI results
    """
    resource = clients.Resource(settings.SWAPI_URL)
    results = []
    while url:
        logger.debug("Current SWAPI URL: %s", url)
        data = resource.get(url)
        logger.debug("Fetched %s items", len(data["results"]))
        results += data["results"]
        url = data["next"]

    return results


def get_planets() -> dict[str, str] | None:
    """
    Fetch all planets from SWAPI.
    Returns:
        Optional[Dict[str, str]]: Dict with url as key and name as value
    """
    return {planet["url"]: planet["name"] for planet in get_all_results("planets")}


def get_people() -> list[dict | None]:
    """
    Fetch all people from SWAPI.
    Returns:
        List[Optional[dict]]: List of people
    """
    return get_all_results("people")


def generate_csv_filename() -> str | os.PathLike:
    """
    Generate a unique filename for CSV file.
    Returns:
        str: Unique filename
    """
    path = os.path.join(settings.MEDIA_ROOT, "starwars", f"{uuid.uuid4()}.csv")
    _validate_file_name_unique_os(path)
    return path


def download_swapi_characters_as_csv(
    path: str | os.PathLike, people_data: list[dict] | None = None, planet_data: dict[str, str] | None = None
) -> str | os.PathLike:
    # path = os.path.join(settings.MEDIA_ROOT, "starwars", f"{uuid.uuid4()}.csv")
    # _validate_file_name_unique_os(path)
    """
    Download all characters from SWAPI and save them to a CSV file.
    Returns:
        Union[str, os.PathLike]: Path to the CSV file
    """
    people = people_data if people_data else get_people()
    planets = planet_data if planet_data else get_planets()

    source = etl.MemorySource(json.dumps(people).encode())

    etl.fromjson(source).cutout("films", "vehicles", "starships", "species", "created", "url").convert(
        "homeworld", lambda v: planets[v]
    ).convert("edited", lambda v: etl.datetimeparser("%Y-%m-%dT%H:%M:%S.%fZ")(v).date()).rename(
        "edited", "date"
    ).tocsv(
        path
    )
    return path


def render_dataset(
    dataset_path: str | os.PathLike, explore: list | None = None, limit: int | None = 10
) -> tuple[str, list[str], bool]:
    """
    Render a dataset as an HTML table.
    Returns:
        Tuple[str, List[str], bool]: HTML table, headers of given table,
        a flag to indicate if there are more rows to show
    """
    table = etl.fromcsv(dataset_path)
    fields = etl.header(table)
    if explore:
        if len(explore) > 1:
            table = etl.aggregate(table, key=explore, aggregation=len, value=explore).rename("value", "count")
        show_load_more = False
    else:
        table = etl.head(table, limit)
        show_load_more = limit < len(table)

    html = etl.MemorySource()
    table.addrownumbers().tohtml(html)
    html = html.getvalue().decode().replace("class='petl'", "class='table table-striped'")

    return html, fields, show_load_more


def _delete_file(file_path: str | os.PathLike):
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error: {file_path} : {e.strerror}")


# @transaction.atomic
def soft_delete_dataset(*, dataset: Dataset) -> Dataset:
    fields = ["is_deleted"]
    data = {"is_deleted": True}
    user, has_updated = model_update(instance=dataset, fields=fields, data=data)
    if has_updated:
        _delete_file(dataset.path)
    else:
        ApplicationError("Dataset has not been deleted")
    return dataset


def delete_dataset(file_path: str | os.PathLike, is_deleted: bool = False) -> str | os.PathLike:
    obj = Dataset.objects.filter(path=file_path, is_deleted=is_deleted).first()

    if obj:
        _delete_file(obj.path)

    obj.delete()

    return file_path


# @transaction.atomic
def create_dataset(file_path: str | os.PathLike) -> Dataset:
    _validate_file_name_unique_DB(file_path)

    obj = Dataset(path=file_path, is_deleted=False)
    obj.full_clean()
    obj.save()

    return obj
