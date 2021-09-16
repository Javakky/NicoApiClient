from typing import Dict, List
from urllib.parse import urlencode, unquote_plus

import math
import requests
import time

from nicovideo_api_client.api.v2.result import SnapshotSearchAPIV2Result
from nicovideo_api_client.constants import END_POINT_URL_V2


class SnapshotSearchAPIV2Request:

    def __init__(self, query: Dict[str, str], limit: int):
        self.query: Dict[str, str] = query
        self.limit = limit

    def request(self) -> SnapshotSearchAPIV2Result:
        if self.limit <= 100:
            self.query["_limit"] = str(self.limit)
        else:
            self.query["_limit"] = "100"

        results: List[SnapshotSearchAPIV2Result] = [SnapshotSearchAPIV2Result(
            self.query,
            requests.get(self.build_url())
        )]

        total_count = int(results[0].total_count())

        if total_count <= self.limit:
            self.limit = total_count

        for pos in range(1, math.ceil(self.limit / 100)):
            self.query["_offset"] = str(pos * 100)
            if self.limit < (pos + 1) * 100:
                self.query["_limit"] = str(self.limit % 100)
            tmp = SnapshotSearchAPIV2Result(self.query, requests.get(self.build_url()))
            while "meta" not in tmp.json() or tmp.status() != 200:
                print("Connection Failed!")
                time.sleep(1.5)
                tmp = SnapshotSearchAPIV2Result(self.query, requests.get(self.build_url()))
            results.append(tmp)

        return SnapshotSearchAPIV2Result(self.query, results)

    def build_url(self, decode: bool = False) -> str:
        query = urlencode(self.query)
        if decode:
            query = unquote_plus(query)
        return END_POINT_URL_V2 + '?' + query
