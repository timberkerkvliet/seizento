import json
import os
from typing import Optional

from seizento.app import AppDataOperator
from seizento.app_data import AppData
from seizento.serializers.app_data_serializer import parse_app_data, serialize_app_data


class JSONFileOperator(AppDataOperator):
    def __init__(self, path: str):
        self._path = path

    def load(self) -> Optional[AppData]:
        if not os.path.exists(self._path):
            return None

        with open(self._path) as f:
            return parse_app_data(json.load(f))

    def save(self, app_data: AppData) -> None:
        with open(self._path, 'w') as f:
            json.dump(serialize_app_data(app_data), f, check_circular=False, indent=4)
