import pytest

from superdevs.starwars.models import Dataset
from superdevs.starwars.tests.factories import DatasetFactory
from superdevs.users.models import User
from superdevs.users.tests.factories import UserFactory
from superdevs.utils.json_utils import SWAPIStoreJSON


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def dataset(db) -> Dataset:
    return DatasetFactory()


@pytest.fixture
def swapi_data_people() -> list[dict] | None:
    people_data = SWAPIStoreJSON("people")
    return people_data.list_items


@pytest.fixture
def swapi_data_planet() -> dict[str, str] | None:
    planet_data = SWAPIStoreJSON("planets")
    return planet_data.list_items


@pytest.fixture
def swapi_data_context() -> tuple[str, list[str], bool]:
    html = """
    <tableclass='tabletable-striped'>
        <thead>
        <tr>
        <th>row</th>
        <th>name</th>
        <th>height</th>
        <th>mass</th>
        <th>hair_color</th>
        <th>skin_color</th>
        <th>eye_color</th>
        <th>birth_year</th>
        <th>gender</th>
        <th>homeworld</th>
        <th>date</th>
        </tr>
        </thead>
        <tbody>
        <tr>
        <tdstyle='text-align:right'>1</td>
        <td>LukeSkywalker</td>
        <td>172</td>
        <td>77</td>
        <td>blond</td>
        <td>fair</td>
        <td>blue</td>
        <td>19BBY</td>
        <td>male</td>
        <td>Tatooine</td>
        <td>2014-12-20</td>
        </tr>
        <tr>
        <tdstyle='text-align:right'>2</td>
        <td>C-3PO</td>
        <td>167</td>
        <td>75</td>
        <td>n/a</td>
        <td>gold</td>
        <td>yellow</td>
        <td>112BBY</td>
        <td>n/a</td>
        <td>Tatooine</td>
        <td>2014-12-20</td>
        </tr>
        <tr>
        <tdstyle='text-align:right'>3</td>
        <td>R2-D2</td>
        <td>96</td>
        <td>32</td>
        <td>n/a</td>
        <td>white,blue</td>
        <td>red</td>
        <td>33BBY</td>
        <td>n/a</td>
        <td>Naboo</td>
        <td>2014-12-20</td>
        </tr>
        <tr>
        <tdstyle='text-align:right'>4</td>
        <td>DarthVader</td>
        <td>202</td>
        <td>136</td>
        <td>none</td>
        <td>white</td>
        <td>yellow</td>
        <td>41.9BBY</td>
        <td>male</td>
        <td>Tatooine</td>
        <td>2014-12-20</td>
        </tr>
        <tr>
        <tdstyle='text-align:right'>5</td>
        <td>LeiaOrgana</td>
        <td>150</td>
        <td>49</td>
        <td>brown</td>
        <td>light</td>
        <td>brown</td>
        <td>19BBY</td>
        <td>female</td>
        <td>Alderaan</td>
        <td>2014-12-20</td>
        </tr>
        <tr>
        <tdstyle='text-align:right'>6</td>
        <td>OwenLars</td>
        <td>178</td>
        <td>120</td>
        <td>brown,grey</td>
        <td>light</td>
        <td>blue</td>
        <td>52BBY</td>
        <td>male</td>
        <td>Tatooine</td>
        <td>2014-12-20</td>
        </tr>
        <tr>
        <tdstyle='text-align:right'>7</td>
        <td>BeruWhitesunlars</td>
        <td>165</td>
        <td>75</td>
        <td>brown</td>
        <td>light</td>
        <td>blue</td>
        <td>47BBY</td>
        <td>female</td>
        <td>Tatooine</td>
        <td>2014-12-20</td>
        </tr>
        <tr>
        <tdstyle='text-align:right'>8</td>
        <td>R5-D4</td>
        <td>97</td>
        <td>32</td>
        <td>n/a</td>
        <td>white,red</td>
        <td>red</td>
        <td>unknown</td>
        <td>n/a</td>
        <td>Tatooine</td>
        <td>2014-12-20</td>
        </tr>
        <tr>
        <tdstyle='text-align:right'>9</td>
        <td>BiggsDarklighter</td>
        <td>183</td>
        <td>84</td>
        <td>black</td>
        <td>light</td>
        <td>brown</td>
        <td>24BBY</td>
        <td>male</td>
        <td>Tatooine</td>
        <td>2014-12-20</td>
        </tr>
        <tr>
        <tdstyle='text-align:right'>10</td>
        <td>Obi-WanKenobi</td>
        <td>182</td>
        <td>77</td>
        <td>auburn,white</td>
        <td>fair</td>
        <td>blue-gray</td>
        <td>57BBY</td>
        <td>male</td>
        <td>Stewjon</td>
        <td>2014-12-20</td>
        </tr>
        </tbody>
    </table>
    """

    fields = [
        "name",
        "height",
        "mass",
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
        "homeworld",
        "date",
    ]
    show_load_more = True

    return html, fields, show_load_more
