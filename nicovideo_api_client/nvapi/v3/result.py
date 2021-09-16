from json import JSONEncoder
from typing import Optional, Dict, Any, List, Union

import requests


class SnapshotSearchNVAPIV3Result:
    def __init__(self, query: Dict[str, str], response: Union[requests.Response, List['SnapshotSearchNVAPIV3Result']]):
        self._json: Optional[Dict[str, Any]] = None
        self.query = query

        if isinstance(response, requests.Response):
            self._json: Optional[Dict[str, Any]] = response.json()
            return

        results: List['SnapshotSearchNVAPIV3Result'] = response

        if len(results) < 1:
            raise Exception("空のリストが渡されました")
        data = {'totalCount': results[0].data()['totalCount'], 'items': []}
        meta = results[0].meta()
        for result in results:
            data['items'].extend(result.data()['items'])
        self._json: Optional[Dict[str, Any]] = {"meta": meta, "data": data}

    def json(self) -> Dict[str, Any]:
        return self._json

    def meta(self) -> Dict[str, Any]:
        if 'meta' not in self.json():
            return {}
        return self.json()['meta']

    def data(self) -> Dict[str, Any]:
        if 'data' not in self.json():
            return {}
        return self.json()['data']

    def items(self) -> List[Dict[str, Any]]:
        if 'items' not in self.data():
            return []
        return self.data()['items']

    def status(self) -> int:
        return self.meta()['status']

    def total_count(self) -> int:
        return self.data()['totalCount']

    def text(self) -> str:
        return JSONEncoder().encode(self.json())
