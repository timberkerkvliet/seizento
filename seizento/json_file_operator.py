import json
import os
from typing import Optional

from seizento.app import AppDataOperator
from seizento.application_data import ApplicationData
from seizento.serializers.app_data_serializer import parse_app_data, serialize_app_data


class JSONFileOperator(AppDataOperator):
    def load(self) -> Optional[ApplicationData]:
        if not os.path.exists('data.json'):
            return None

        with open('data.json') as f:
            return parse_app_data(json.load(f))

    def save(self, app_data: ApplicationData) -> None:
        with open('data.json') as f:
            json.dump(serialize_app_data(app_data), f)
