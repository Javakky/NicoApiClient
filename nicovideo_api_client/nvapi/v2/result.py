from json import JSONEncoder
from typing import Optional, Dict, Any, List, Union

import requests


class SnapshotSearchNVAPIV2Result:
    def __init__(self, query: Dict[str, str], response: Union[requests.Response, List['SnapshotSearchNVAPIV2Result']]):
        self._json: Optional[Dict[str, Any]] = None
        self.query = query

        if isinstance(response, requests.Response):
            self._json: Optional[Dict[str, Any]] = response.json()
            return

        results: List['SnapshotSearchNVAPIV2Result'] = response

        if len(results) < 1:
            raise Exception("空のリストが渡されました")
        data = results[0].data()
        meta = results[0].meta()
        for result in results:
            data['mylist']['items'].extend(result.mylist()['items'])
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

    def mylist(self) -> Dict[str, Any]:
        if 'data' not in self.json():
            return {}
        return self.data()['mylist']

    def status(self) -> int:
        return self.meta()['status']

    def description(self) -> str:
        return self.mylist()['description']

    def items(self) -> List[Dict[str, Any]]:
        return self.mylist()['items']

    def text(self) -> str:
        return JSONEncoder().encode(self.json())

    def total_item_count(self):
        return self.mylist()['totalItemCount']
