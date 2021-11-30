from typing import Dict, Union

from nicovideo_api_client.api.v2.request import SnapshotSearchAPIV2Request


class SnapshotSearchAPIV2UserAgent:
    def __init__(self, query: Dict[str, str], limit: int):
        self._query: Dict[str, str] = query
        self._limit: int = limit

    def user_agent(
        self, product: str = None, version: Union[int, str] = None, comment: str = None
    ) -> SnapshotSearchAPIV2Request:
        """
        レスポンスの要素数を指定する。

        :param
            product: HTTPリクエストヘッダのUser-Agentに指定するプロダクト名
            version: HTTPリクエストヘッダのUser-Agentに指定するプロダクトバージョン
            product: HTTPリクエストヘッダのUser-Agentに指定するコメント
        :return: リクエストオブジェクト
        """

        if product is None or product == "":
            raise Exception("User-Agentのプロダクト名の指定は必須です")
        elif version is None or version == "":
            raise Exception("User-Agentのプロダクトバージョンの指定は必須です")
        else:
            if version is int:
                version = str(version)
            user_agent = (product, version, comment)
        return SnapshotSearchAPIV2Request(self._query, self._limit, user_agent)
