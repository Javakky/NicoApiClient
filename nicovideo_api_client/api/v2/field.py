from typing import Dict, Set, Union

from nicovideo_api_client.api.v2.sort import SnapshotSearchAPIV2Sort
from nicovideo_api_client.constants import FieldType


class SnapshotSearchAPIV2Fields:
    def __init__(self, query: Dict[str, str]):
        self._fields: Set[str] = set()
        self._query: Dict[str, str] = query

    def field(self, fields: Set[FieldType]) -> "SnapshotSearchAPIV2Sort":
        """
        レスポンスの返すフィールドタイプを指定する。

        :param fields: レスポンスの返すフィールドタイプ一覧
        :return: ソートタイプ指定オブジェクト
        """
        self._fields = sorted(list(map(lambda x: x.value, fields)))
        if len(self._fields) > 0:
            self._query["fields"] = ",".join(self._fields)
        return SnapshotSearchAPIV2Sort(self._query)

    def _and(self, keyword: Union[str, list[str]]) -> "SnapshotSearchAPIV2Fields":
        if type(keyword) is str:
            self._query["q"] += " " + keyword
        elif type(keyword) is list:
            self._query["q"] += " " + " OR ".join(keyword)
        else:
            raise TypeError("検索キーワードには str または list が指定されるべきです")

        return self
