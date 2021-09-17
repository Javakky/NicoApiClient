from typing import Dict, List, Tuple
from urllib.parse import urlencode, unquote_plus

import math
import requests
import time

from nicovideo_api_client.api.v2.result import SnapshotSearchAPIV2Result
from nicovideo_api_client.constants import END_POINT_URL_V2


class SnapshotSearchAPIV2Request:

    def __init__(self, query: Dict[str, str], limit: int):
        self._query: Dict[str, str] = query
        self._limit = limit

    def request(self, timeout: float = 400.0) -> SnapshotSearchAPIV2Result:
        if self._limit <= 100:
            self._query["_limit"] = str(self._limit)
        else:
            self._query["_limit"] = "100"

        total_time = 0.0

        (response, response_time) = self._request(timeout)
        total_time += response_time

        results: List[SnapshotSearchAPIV2Result] = [response]

        total_count = int(results[0].total_count())

        if total_count <= self._limit:
            self._limit = total_count

        for pos in range(1, math.ceil(self._limit / 100)):
            self._query["_offset"] = str(pos * 100)
            if self._limit < (pos + 1) * 100:
                self._query["_limit"] = str(self._limit % 100)

            time.sleep(response_time)

            while True:
                (response, response_time) = self._request(timeout)
                total_time += response_time
                if total_time > timeout:
                    raise TimeoutError("通信がタイムアウトしました")
                if "meta" in response.json() or response.status() == 200:
                    break
                print("Connection Failed!")
                time.sleep(response_time)
                
            results.append(response)
        return SnapshotSearchAPIV2Result(self._query, results)

    def _request(self, timeout: float) -> Tuple[SnapshotSearchAPIV2Result, float]:
        response = requests.get(self.build_url(), timeout=(timeout / 4, timeout * 3 / 4))
        total_time = response.elapsed.total_seconds()
        tmp = SnapshotSearchAPIV2Result(self._query, response)
        return tmp, total_time

    def build_url(self, decode: bool = True) -> str:
        query = urlencode(self._query)
        if decode:
            query = unquote_plus(query)
        return END_POINT_URL_V2 + '?' + query
