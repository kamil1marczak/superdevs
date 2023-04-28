import json
import os

from django.conf import settings


class SWAPIStoreJSON:
    def __init__(self, json_file_name):
        self.file_path = os.path.join(settings.APPS_DIR, "fixture_files", f"{json_file_name}.json")
        # self.filename = json_file_name

    def clear_file(self):
        with open(self.file_path, "w") as file:
            json.dump([], file)

    def add(self, item):
        with open(self.file_path, "r+") as file:
            calculations = json.load(file)
            calculations.append(item)
            file.seek(0)
            json.dump(calculations, file)

    @property
    def list_items(self):
        with open(self.file_path) as file:
            swapi_data = json.load(file)

        return [swapi_item for swapi_item in swapi_data]
