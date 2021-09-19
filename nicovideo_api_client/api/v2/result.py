import statistics
from json import JSONEncoder
from typing import Optional, Dict, Any, List, Union

import math
import requests

from nicovideo_api_client.constants import FieldType


class SnapshotSearchAPIV2Result:
    """
    `レスポンス仕様 <https://site.nicovideo.jp/search-api-docs/snapshot#%E3%83%AC%E3%82%B9%E3%83%9D%E3%83%B3%E3%82%B9>`_
    """
    def __init__(self, query: Dict[str, str], response: Union[requests.Response, List['SnapshotSearchAPIV2Result']]):
        self._fields: List[str] = query["fields"].split(",") if "fields" in query else []
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
        """
        レスポンスを Dict オブジェクトとして返す。
        """
        return self._json

    def meta(self) -> Dict[str, Any]:
        """
        リクエストのメタ情報 (HTTP Status など) を返す。
        """
        if 'meta' not in self.json():
            return {}
        return self.json()['meta']

    def data(self) -> List[Dict[str, Any]]:
        """
        レスポンスの本体データを Dict オブジェクト形式で返す。
        """
        if 'data' not in self.json():
            return []
        return self.json()['data']

    def sum_view_counter(self) -> int:
        """
        レスポンスに含まれる再生回数の合計を返す。
        """
        if FieldType.VIEW_COUNTER.value not in self._fields:
            raise Exception("フィールドに viewCounter が指定されていません")
        return sum(list(map(lambda x: x[FieldType.VIEW_COUNTER.value], self.data())))

    def avg_view_counter(self) -> int:
        """
        レスポンスに含まれる再生回数の平均を返す。
        """
        if FieldType.VIEW_COUNTER.value not in self._fields:
            raise Exception("フィールドに viewCounter が指定されていません")
        return statistics.mean(list(map(lambda x: x[FieldType.VIEW_COUNTER.value], self.data())))

    def center_view_counter(self) -> int:
        """
        レスポンスに含まれる再生回数の中央値を返す。
        """
        if FieldType.VIEW_COUNTER.value not in self._fields:
            raise Exception("フィールドに viewCounter が指定されていません")
        return self.data()[math.floor(self.total_count() / 2)][FieldType.VIEW_COUNTER.value]

    def status(self) -> int:
        """
        HTTP レスポンスのStatus を返す。

        複数回に分割リクエストした場合、エラー処理ができていないためここに辿り着いた時点で 200

        TODO: 分割リクエストにエラー対応を実装
        """
        return self.meta()['status']

    def total_count(self) -> int:
        """
        レスポンスに含まれる件数
        """
        return self.meta()['totalCount']

    def text(self) -> str:
        """
        レスポンスを文字列形式で表す
        """
        return JSONEncoder().encode(self.json())
