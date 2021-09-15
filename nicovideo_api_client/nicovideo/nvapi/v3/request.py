import math
import time
import urllib
from typing import Dict, List
from urllib.parse import urlencode, unquote_plus

import requests

from nicovideo_api_client.nicovideo.api.v2.result import SnapshotSearchAPIV2Result
from nicovideo_api_client.nicovideo.nvapi.v3.result import SnapshotSearchNVAPIV3Result


class SnapshotSearchNVAPIV3Request:

    def __init__(self, endpoint: str, query: Dict[str, str], limit: int):
        self.endpoint = endpoint
        self.query: Dict[str, str] = query
        self.limit = limit

    def get(self, url: str):
        return requests.get(url, headers={'X-Frontend-Id': '6'})

    def request(self) -> SnapshotSearchNVAPIV3Result:
        if self.limit <= 100:
            self.query["pageSize"] = str(self.limit)
        else:
            self.query["pageSize"] = "100"

        results: List[SnapshotSearchNVAPIV3Result] = [SnapshotSearchNVAPIV3Result(
            self.query,
            self.get(self.build_url())
        )]

        total_count = int(results[0].total_count())

        if total_count <= self.limit:
            self.limit = total_count

        for pos in range(1, math.ceil(self.limit / 100)):
            self.query["page"] = str(pos * 100)
            if self.limit < (pos + 1) * 100:
                self.query["pageSize"] = str(self.limit % 100)
            tmp = SnapshotSearchNVAPIV3Result(self.query, self.get(self.build_url()))
            while "meta" not in tmp.json() or tmp.status() != 200:
                print("Connection Failed!")
                time.sleep(1.5)
                tmp = SnapshotSearchAPIV2Result(self.query, self.get(self.build_url()))
            results.append(tmp)

        return SnapshotSearchNVAPIV3Result(self.query, results)

    def build_url(self, decode: bool = False) -> str:
        query = urlencode(self.query)
        if decode:
            query = urllib.parse.unquote_plus(query)
        return self.endpoint + '?' + unquote_plus(query)
