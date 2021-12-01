from typing import Dict, Union

from nicovideo_api_client.api.v2.request import SnapshotSearchAPIV2Request


class SnapshotSearchAPIV2UserAgent:
    def __init__(self, query: Dict[str, str], limit: int):
        self._query: Dict[str, str] = query
        self._limit: int = limit

    def user_agent(
        self, product: str, version: Union[int, str], comment: str = ""
    ) -> SnapshotSearchAPIV2Request:
        """
        レスポンスの要素数を指定する。

        :param product: HTTPリクエストヘッダのUser-Agentに指定するプロダクト名
        :param version: HTTPリクエストヘッダのUser-Agentに指定するプロダクトバージョン
        :param comment: HTTPリクエストヘッダのUser-Agentに指定するコメント
        :return: リクエストオブジェクト
        """

        if product.isspace():
            raise ValueError("User-Agentのプロダクト名に空白文字のみを指定することはできません")
        if version.isspace():
            raise ValueError("User-Agentのプロダクトバージョンに空白文字のみを指定することはできません")
        if version is int:
            version = str(version)
        user_agent = (product, version, comment)
        return SnapshotSearchAPIV2Request(self._query, self._limit, user_agent)
