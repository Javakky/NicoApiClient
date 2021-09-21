from typing import Dict

from nicovideo_api_client.api.v2.field import SnapshotSearchAPIV2Fields
from nicovideo_api_client.constants import FieldType


class SnapshotSearchAPIV2Targets:
    def __init__(self, *targets: FieldType):
        list_targets = list(targets)
        if len(list_targets) == 0:
            raise Exception("targets が設定されていません")
        self._query: Dict[str, str] = {'targets': ','.join(map(lambda x: x.value, list_targets))}

    def query(self, keyword: str) -> SnapshotSearchAPIV2Fields:
        """
        検索クエリ(キーワード)を指定する。

        `クエリ文字列仕様 <https://site.nicovideo.jp/search-api-docs/snapshot#%EF%BC%8A1-
        %E3%82%AF%E3%82%A8%E3%83%AA%E6%96%87%E5%AD%97%E5%88%97%E4%BB%95%E6%A7%98>`_
        に沿った値を入力することで AND, OR 検索など複数のキーワードを含めた検索を行うことができる。

        TODO: AND・OR検索を実装する

        :param keyword: 検索するキーワード
        :return: レスポンスフィールドのタイプ指定オブジェクト
        """
        self._query['q'] = keyword
        return SnapshotSearchAPIV2Fields(self._query)
