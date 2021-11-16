from typing import Dict, Union, Set

from nicovideo_api_client.api.v2.field import SnapshotSearchAPIV2Fields
from nicovideo_api_client.constants import FieldType


class SnapshotSearchAPIV2Targets:
    def __init__(self, *targets: FieldType):
        list_targets = list(targets)
        if len(list_targets) == 0:
            raise Exception("targets が設定されていません")
        self._query: Dict[str, str] = {
            "targets": ",".join(map(lambda x: x.value, list_targets))
        }

    def single_query(self, keyword: Union[str, list[str]]) -> SnapshotSearchAPIV2Fields:
        """
        検索クエリ(キーワード)を指定する。

        `クエリ文字列仕様 <https://site.nicovideo.jp/search-api-docs/snapshot#%EF%BC%8A1-
        %E3%82%AF%E3%82%A8%E3%83%AA%E6%96%87%E5%AD%97%E5%88%97%E4%BB%95%E6%A7%98>`_
        に沿った値を入力することでキーワードを含めた検索を行うことができる。

        :param
            keyword: 検索するキーワード。文字列または文字列を要素に持つリスト。
        :return: レスポンスフィールドのタイプ指定オブジェクト
        """

        if keyword == "":
            raise Exception("キーワードなし検索を行うにはno_keywordメソッドを指定する必要があります")
        self._query["q"] = None
        SnapshotSearchAPIV2And(self._query).and_(keyword)
        return SnapshotSearchAPIV2Fields(self._query)

    def query(self, keyword: Union[str, list[str]]) -> "SnapshotSearchAPIV2And":
        """
        AND・OR検索を用いて検索クエリ(キーワード)を指定する。

        `クエリ文字列仕様 <https://site.nicovideo.jp/search-api-docs/snapshot#%EF%BC%8A1-
        %E3%82%AF%E3%82%A8%E3%83%AA%E6%96%87%E5%AD%97%E5%88%97%E4%BB%95%E6%A7%98>`_
        に沿った値を入力することで AND, OR 検索など複数のキーワードを含めた検索を行うことができる。

        :param
            keyword: 検索するキーワード。文字列または文字列を要素に持つリスト。
        :return: レスポンスアンドのタイプ指定オブジェクト
        """

        self._query["q"] = None
        if keyword == "":
            raise Exception("キーワードなし検索を行うにはno_keywordメソッドを指定する必要があります")
        return SnapshotSearchAPIV2And(self._query).and_(keyword)

    def no_keyword(self) -> SnapshotSearchAPIV2Fields:
        """
        キーワードなし検索を行う。

        `クエリ文字列仕様 <https://site.nicovideo.jp/search-api-docs/snapshot#%EF%BC%8A1-
        %E3%82%AF%E3%82%A8%E3%83%AA%E6%96%87%E5%AD%97%E5%88%97%E4%BB%95%E6%A7%98>`_
        q=自体の省略はできません。
        負荷の高い検索となりますので、filtersと併用しヒット件数を10万件以内に絞り込んだ上でご利用ください。

        :return: レスポンスフィールドのタイプ指定オブジェクト
        """
        self._query["q"] = ""
        return SnapshotSearchAPIV2Fields(self._query)


class SnapshotSearchAPIV2And:
    def __init__(self, query: Dict[str, str]):
        self._query: Dict[str, str] = query

    def field(self, fields: Set[FieldType]):
        return SnapshotSearchAPIV2Fields(self._query).field(fields)

    def _arrage_keyword(self, keyword: str):
        if " " in keyword:
            raise Exception("検索ワードに半角スペースが含まれています")
        if keyword == "OR":
            keyword = '"OR"'
        if self._query["q"] is None:
            self._query["q"] = keyword
        else:
            self._query["q"] += " " + keyword

    def and_(self, keyword: Union[str, list[str]]):
        if type(keyword) is str:
            self._arrage_keyword(keyword)
        elif type(keyword) is list:
            for k in keyword:
                self._arrage_keyword(k)
                if k != keyword[-1]:
                    self._query["q"] += " OR"
        else:
            raise TypeError("検索キーワードには str または list が指定されるべきです")

        return self
