from datetime import datetime
from typing import Dict, List, Optional, Union


TypeOp = Dict[str, Union[str, bool, int, List['TypeOp'], 'TypeOp']]


class JsonFilterOperator:
    """
    `jsonFilter` による絞り込みの条件を表現するクラス。

    基本的にはこのオブジェクト1つで検索条件を表現するが、入子的に複数の検索条件が設定されることがある。
    """
    def __init__(self, json_: TypeOp):
        self.json: TypeOp = json_

    @staticmethod
    def unit(term: 'JsonFilterTerm') -> 'JsonFilterOperator':
        """
        単一の絞り込み要素のみで絞り込むことを明示的に宣言する。

        基本的に要素のみでの指定ができるため、利用する必要がない。

        Note: deprecated

        :param term: 絞り込み要素
        :return: 絞り込み条件オブジェクト
        """
        return JsonFilterOperator(term.json)

    @staticmethod
    def not_(
            term: 'JsonFilterOperator'
    ) -> 'JsonFilterOperator':
        """
        与えられた絞り込み要素の論理否定を表現する絞り込み条件。

        :param term: 否定したい絞り込み要素
        :return: 絞り込み条件オブジェクト
        """
        json_: TypeOp = {
            "type": "not",
            "filter": term.json
        }
        return JsonFilterOperator(json_)

    @staticmethod
    def _binary(
            op_name: str,
            left: 'JsonFilterOperator',
            right: 'JsonFilterOperator'
    ) -> 'JsonFilterOperator':
        json_: TypeOp = {
            "type": op_name,
            "filters": []
        }
        json_["filters"].append(left.json)
        json_["filters"].append(right.json)
        return JsonFilterOperator(json_)

    @staticmethod
    def or_(
            left: 'JsonFilterOperator',
            right: 'JsonFilterOperator'
    ) -> 'JsonFilterOperator':
        """
        2つの絞り込み要素のどちらかが正しいことを表す絞り込み条件。

        :param left: 絞り込み要素 1
        :param right: 絞り込み要素 2
        :return: 絞り込み条件オブジェクト
        """
        return JsonFilterOperator._binary("or", left, right)

    @staticmethod
    def and_(
            left: 'JsonFilterOperator',
            right: 'JsonFilterOperator'
    ) -> 'JsonFilterOperator':
        """
        2つの絞り込み要素の両方が正しいことを表す絞り込み条件。

        :param left: 絞り込み要素 1
        :param right: 絞り込み要素 2
        :return: 絞り込み条件オブジェクト
        """
        return JsonFilterOperator._binary("and", left, right)


class JsonFilterTerm(JsonFilterOperator):
    """
    `FieldType` と値の関係が正しいかを示す検索要素。

    `equal` と `range` の2種類がある。

    TODO: equal 絞り込みを実装する。
    """
    def __init__(self):
        super().__init__({})

    @staticmethod
    def set_range_view(
            from_: Optional[int] = None,
            to_: Optional[int] = None,
            include_lower: bool = True,
            include_upper: bool = True,
    ) -> 'JsonFilterTerm':
        """
        再生回数が与えられた範囲内かを調べる検索要素。

        :param from_: 再生回数の下限
        :param to_: 再生回数の上限
        :param include_lower: from_ を含むかどうか
        :param include_upper: to_ を含むかどうか
        :return: 絞り込み要素オブジェクト
        """
        term: JsonFilterTerm = JsonFilterTerm()
        if from_ is None and to_ is None:
            raise Exception("上限も下限も指定されていません")
        json_: Dict[str, Union[str, bool, int]] = {
            "type": "range",
            "field": "viewCounter"
        }
        if from_ is not None:
            json_["from"] = from_
        if to_ is not None:
            json_["to"] = to_
        if include_lower:
            json_["include_lower"] = include_lower
        if include_upper:
            json_["include_upper"] = include_upper
        term.json = json_
        return term

    @staticmethod
    def set_range_time(
            from_: Optional[datetime] = None,
            to_: Optional[datetime] = None,
            include_lower: bool = True,
            include_upper: bool = True,
    ) -> 'JsonFilterTerm':
        """
        投稿時刻が与えられた範囲内かを調べる検索要素。

        :param from_: 投稿時刻の最古
        :param to_: 投稿時刻の最新
        :param include_lower: from_ を含むかどうか
        :param include_upper: to_ を含むかどうか
        :return: 絞り込み要素オブジェクト
        """
        term: JsonFilterTerm = JsonFilterTerm()
        if from_ is None and to_ is None:
            raise Exception("開始時刻も終了時刻も指定されていません")
        json_: Dict[str, Union[str, bool]] = {
            "type": "range",
            "field": "startTime"
        }
        if from_ is not None:
            json_["from"] = from_.strftime('%Y-%m-%dT%H:%M:%S+09:00')
        if to_ is not None:
            json_["to"] = to_.strftime('%Y-%m-%dT%H:%M:%S+09:00')
        if include_lower:
            json_["include_lower"] = include_lower
        if include_upper:
            json_["include_upper"] = include_upper
        term.json = json_
        return term
