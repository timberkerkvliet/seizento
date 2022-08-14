import json
import os
from typing import Optional

from seizento.app import AppDataOperator
from seizento.app_data import AppData
from seizento.serializers.app_data_serializer import parse_app_data, serialize_app_data


class JSONFileOperator(AppDataOperator):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def load(self) -> Optional[AppData]:
        if not os.path.exists(self._file_path):
            return None

        with open(self._file_path) as f:
            return parse_app_data(json.load(f))

    def save(self, app_data: AppData) -> None:
        with open(self._file_path, 'w') as f:
            json.dump(serialize_app_data(app_data), f, check_circular=False, indent=4)
