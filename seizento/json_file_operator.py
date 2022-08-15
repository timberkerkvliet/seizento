import json
import os
from typing import Optional

from seizento.app import AppDataOperator
from seizento.app_data import AppData
from seizento.serializers.app_data_serializer import parse_app_data, serialize_app_data


class JSONFileOperator(AppDataOperator):
    DATA_FOLDER = '/app-data'
    DATA_FILE = '/app-data/data.json'

    def __init__(self):
        if not os.path.exists(self.DATA_FOLDER):
            os.makedirs(self.DATA_FOLDER)

    def load(self) -> Optional[AppData]:
        if not os.path.exists(self.DATA_FILE):
            return None

        with open(self.DATA_FILE) as f:
            return parse_app_data(json.load(f))

    def save(self, app_data: AppData) -> None:
        with open(self.DATA_FILE, 'w') as f:
            json.dump(serialize_app_data(app_data), f, check_circular=False, indent=4)
