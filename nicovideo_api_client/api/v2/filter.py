import urllib.parse
from json import JSONEncoder
from typing import Dict, Union

from nicovideo_api_client.api.v2.json_filter import JsonFilterOperator, JsonFilterTerm
from nicovideo_api_client.api.v2.limit import SnapshotSearchAPIV2Limit
from nicovideo_api_client.api.v2.simple_filter import SnapshotSearchAPIV2SimpleFilter


class SnapshotSearchAPIV2Filter:
    def __init__(self, query: Dict[str, str]):
        self._query: Dict[str, str] = query

    def simple_filter(self) -> SnapshotSearchAPIV2SimpleFilter:
        """
        絞り込みにシンプルな `filters` を利用することを宣言する。

        :return: フィルタリング要素指定オブジェクト
        """
        return SnapshotSearchAPIV2SimpleFilter(self._query)

    def json_filter(
            self,
            op: Union[JsonFilterOperator, JsonFilterTerm]
    ) -> SnapshotSearchAPIV2Limit:
        """
        `JsonFilterOperator` を使って表現した条件から、 `jsonFilter` を利用して絞り込む。

        :param op: 絞り込み条件
        :return: リクエスト上限設定オブジェクト
        """
        self._query["jsonFilter"] = urllib.parse.quote_plus(JSONEncoder().encode(op.json))
        return SnapshotSearchAPIV2Limit(self._query)
