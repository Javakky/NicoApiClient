from typing import Dict

from nicovideo_api_client.api.v2.filter import SnapshotSearchAPIV2Filter
from nicovideo_api_client.constants import FieldType, sort_types


class SnapshotSearchAPIV2Sort:
    def __init__(self, query: Dict[str, str]):
        self._query: Dict[str, str] = query

    def sort(self, sort_type: FieldType, reverse: bool = False) -> SnapshotSearchAPIV2Filter:
        """
        ソートタイプを指定する。

        :param sort_type: ソートに利用するフィールドタイプ
        :param reverse: True: 昇順, False (デフォルト): 降順
        :return: フィルター指定オブジェクト
        """
        if sort_type not in sort_types:
            raise Exception("不正なソートタイプ")
        self._query['_sort'] = ('+' if reverse else '-') + sort_type.value
        return SnapshotSearchAPIV2Filter(self._query)
