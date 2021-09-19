from typing import Dict

from nicovideo_api_client.api.v2.request import SnapshotSearchAPIV2Request


class SnapshotSearchAPIV2Limit:

    def __init__(self, query: Dict[str, str]):
        self._query: Dict[str, str] = query

    def limit(self, limit: int = 10) -> SnapshotSearchAPIV2Request:
        """
        レスポンスの要素数を指定する。

        :param limit: レスポンスの要素数の上限。デフォルトは API 仕様に則り 10件。
        本来の件数上限は 100件だが、分割リクエストを送るためそれ以上を指定できる。
        :return: リクエストオブジェクト
        """
        return SnapshotSearchAPIV2Request(self._query, limit)
