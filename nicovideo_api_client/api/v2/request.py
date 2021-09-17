from typing import Dict, List, Tuple
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

    def request(self, timeout: float = 400.0) -> SnapshotSearchAPIV2Result:
        if self.limit <= 100:
            self.query["_limit"] = str(self.limit)
        else:
            self.query["_limit"] = "100"

        total_time = 0.0
        wait_time = 0.0

        (response, add_time) = self._request(timeout)
        total_time += add_time

        results: List[SnapshotSearchAPIV2Result] = [response]

        total_count = int(results[0].total_count())

        if total_count <= self.limit:
            self.limit = total_count

        for pos in range(1, math.ceil(self.limit / 100)):
            self.query["_offset"] = str(pos * 100)
            if self.limit < (pos + 1) * 100:
                self.query["_limit"] = str(self.limit % 100)

            wait_time = total_time - wait_time
            time.sleep(wait_time)
            wait_time = total_time

            while True:
                (response, add_time) = self._request(timeout)
                total_time += add_time
                if total_time > timeout:
                    raise TimeoutError("通信がタイムアウトしました")
                if "meta" in response.json() or response.status() == 200: break
                print("Connection Failed!")
                time.sleep(1.5)
                
            results.append(response)
        return SnapshotSearchAPIV2Result(self.query, results)

    def _request(self, timeout: float) -> Tuple[SnapshotSearchAPIV2Result, float]:
        response = requests.get(self.build_url(), timeout = (timeout / 4, timeout * 3 / 4))
        total_time = response.elapsed.total_seconds()
        tmp = SnapshotSearchAPIV2Result(self.query, response)
        return (tmp, total_time)

    def build_url(self, decode: bool = False) -> str:
        query = urlencode(self.query)
        if decode:
            query = unquote_plus(query)
        return END_POINT_URL_V2 + '?' + query
