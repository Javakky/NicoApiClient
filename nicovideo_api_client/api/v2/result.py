import statistics
from json import JSONEncoder
from typing import Optional, Dict, Any, List, Union

import math
import requests

from nicovideo_api_client.constants import FieldType


class SnapshotSearchAPIV2Result:
    def __init__(self, query: Dict[str, str], response: Union[requests.Response, List['SnapshotSearchAPIV2Result']]):
        self.fields: List[str] = query["fields"].split(",") if "fields" in query else []
        self._json: Optional[Dict[str, Any]] = None

        if isinstance(response, requests.Response):
            self._json: Optional[Dict[str, Any]] = response.json()
            return

        results: List['SnapshotSearchAPIV2Result'] = response

        if len(results) < 1:
            raise Exception("空のリストが渡されました")
        data = []
        meta = results[0].json()["meta"]
        for result in results:
            data.extend(result.json()["data"])
        self._json: Optional[Dict[str, Any]] = {"meta": meta, "data": data}

    def json(self) -> Dict[str, Any]:
        return self._json

    def meta(self) -> Dict[str, Any]:
        if 'meta' not in self.json():
            return {}
        return self.json()['meta']

    def data(self) -> List[Dict[str, Any]]:
        if 'data' not in self.json():
            return []
        return self.json()['data']

    def sum_view_counter(self) -> int:
        if FieldType.VIEW_COUNTER.value not in self.fields:
            raise Exception("フィールドに viewCounter が指定されていません")
        return sum(list(map(lambda x: x[FieldType.VIEW_COUNTER.value], self.data())))

    def avg_view_counter(self) -> int:
        if FieldType.VIEW_COUNTER.value not in self.fields:
            raise Exception("フィールドに viewCounter が指定されていません")
        return statistics.mean(list(map(lambda x: x[FieldType.VIEW_COUNTER.value], self.data())))

    def center_view_counter(self) -> int:
        if FieldType.VIEW_COUNTER.value not in self.fields:
            raise Exception("フィールドに viewCounter が指定されていません")
        return self.data()[math.floor(self.total_count() / 2)][FieldType.VIEW_COUNTER.value]

    def status(self) -> int:
        return self.meta()['status']

    def total_count(self) -> int:
        return self.meta()['totalCount']

    def text(self) -> str:
        return JSONEncoder().encode(self.json())
