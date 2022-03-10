from typing import Dict, Optional, Set, Union

from nicovideo_api_client.api.v2.field import SnapshotSearchAPIV2Fields
from nicovideo_api_client.api.v2.sort import SnapshotSearchAPIV2Sort
from nicovideo_api_client.constants import FieldType


class SnapshotSearchAPIV2Targets:
    def __init__(self, *targets: FieldType):
        list_targets = list(targets)
        if len(list_targets) == 0:
            raise Exception("targets が設定されていません")
        self._query: Dict[str, str] = {"targets": ",".join(map(lambda x: x.value, list_targets))}

    def single_query(self, keyword: str) -> SnapshotSearchAPIV2Fields:
        """
        検索クエリ(キーワード)を指定する。

        `クエリ文字列仕様 <https://site.nicovideo.jp/search-api-docs/snapshot#%EF%BC%8A1-
        %E3%82%AF%E3%82%A8%E3%83%AA%E6%96%87%E5%AD%97%E5%88%97%E4%BB%95%E6%A7%98>`_
        に沿った値を入力することでキーワードを含めた検索を行うことができる。

        文字列を直接クエリに渡すため、キーワードに半角スペースやORを含めることでAND・OR検索を行うことができる。

        :param keyword: 検索するキーワード(文字列型)
        :return: レスポンスフィールドのタイプ指定オブジェクト
        """
        if type(keyword) is not str:
            raise TypeError("single_queryで指定するキーワードは str であるべきです")
        elif keyword == "":
            raise Exception("キーワードなし検索を行うにはno_keywordメソッドを指定する必要があります")
        self._query["q"] = keyword
        return SnapshotSearchAPIV2Fields(self._query)

    def query(self, keyword: list[str], exclude: Optional[list[str]] = None) -> "SnapshotSearchAPIV2And":
        """
        AND・OR検索を用いて検索クエリ(キーワード)を指定する。

        `クエリ文字列仕様 <https://site.nicovideo.jp/search-api-docs/snapshot#%EF%BC%8A1-
        %E3%82%AF%E3%82%A8%E3%83%AA%E6%96%87%E5%AD%97%E5%88%97%E4%BB%95%E6%A7%98>`_
        に沿った値を入力することで AND, OR 検索など複数のキーワードを含めた検索を行うことができる。

        :param exclude: NOT 検索で使用するキーワード
        :param keyword: 検索するキーワード。文字列を要素に持つリストの形式になっており、複数要素があれば OR で連結される。
        :return: レスポンスアンドのタイプ指定オブジェクト
        """

        if exclude is None:
            exclude = []
        if type(keyword) is not list or len(keyword) < 1:
            raise Exception("キーワードなし検索を行うにはno_keywordメソッドを指定する必要があります")
        return SnapshotSearchAPIV2And(self._query, exclude).and_(keyword)

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


class SnapshotSearchAPIV2And(SnapshotSearchAPIV2Fields):
    def __init__(self, query: Dict[str, str], exclude: list[str]):
        super().__init__(query)
        self.exclude = exclude

    def field(self, fields: Set[FieldType]) -> SnapshotSearchAPIV2Sort:
        if self._query["q"] == "":
            raise Exception("NOT検索のみを実行することはできません")
        for e in self.exclude:
            self._arrange_keyword(e, exclude=True)
        return super().field(fields)

    def _arrange_keyword(self, keyword: str, exclude: bool = False):
        """
        キーワードを適切な形でクエリに指定する。
        :param keyword: クエリのqキーに指定するための文字列
        """
        # フレーズ検索かどうかの判定(" "は" OR "も含んでいる)
        if (
            ((keyword[0] != '"' and keyword[-1] != '"') and " " in keyword)
            or keyword[0] == "-"
            or '"' in keyword
            or "\\" in keyword
        ):
            keyword = '"' + keyword.replace("\\", "\\\\").replace('"', '\\"') + '"'
        elif keyword == "OR":
            keyword = '"OR"'
        if exclude:
            keyword = "-" + keyword
        if "q" not in self._query.keys():
            self._query["q"] = keyword
        else:
            self._query["q"] += " " + keyword

    def and_(self, keyword: Union[str, list[str]]) -> "SnapshotSearchAPIV2And":
        """
        AND 検索に利用する。
        NOT 検索に必要なパラメータは `query()` で指定する。
        :param keyword: 検索するキーワード。文字列または文字列を要素に持つリスト。リストにする場合は OR で連結される。
        """
        if type(keyword) is str:
            self._arrange_keyword(keyword)
        elif type(keyword) is list:
            for k in keyword:
                self._arrange_keyword(k)
                if k != keyword[-1]:
                    self._query["q"] += " OR"
        else:
            raise TypeError("検索キーワードには str または list が指定されるべきです")

        return self
