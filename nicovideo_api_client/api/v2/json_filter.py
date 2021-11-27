from datetime import datetime
from typing import Dict, List, Optional, Type, Union

from nicovideo_api_client.constants import FieldType

TypeOp = Dict[str, Union[str, bool, int, List["TypeOp"], "TypeOp"]]


class JsonFilterOperator:
    """
    `jsonFilter` による絞り込みの条件を表現するクラス。

    基本的にはこのオブジェクト1つで検索条件を表現するが、入子的に複数の検索条件が設定されることがある。
    """

    def __init__(self, json_: TypeOp):
        self.json: TypeOp = json_

    @staticmethod
    def unit(term: "JsonFilterTerm") -> "JsonFilterOperator":
        """
        単一の絞り込み要素のみで絞り込むことを明示的に宣言する。

        基本的に要素のみでの指定ができるため、利用する必要がない。

        Note: deprecated

        :param term: 絞り込み要素
        :return: 絞り込み条件オブジェクト
        """
        return JsonFilterOperator(term.json)

    @staticmethod
    def not_(term: "JsonFilterOperator") -> "JsonFilterOperator":
        """
        与えられた絞り込み要素の論理否定を表現する絞り込み条件。

        :param term: 否定したい絞り込み要素
        :return: 絞り込み条件オブジェクト
        """
        json_: TypeOp = {"type": "not", "filter": term.json}
        return JsonFilterOperator(json_)

    @staticmethod
    def _binary(
        op_name: str, left: "JsonFilterOperator", right: "JsonFilterOperator"
    ) -> "JsonFilterOperator":
        json_: TypeOp = {"type": op_name, "filters": []}
        json_["filters"].append(left.json)
        json_["filters"].append(right.json)
        return JsonFilterOperator(json_)

    @staticmethod
    def or_(
        left: "JsonFilterOperator", right: "JsonFilterOperator"
    ) -> "JsonFilterOperator":
        """
        2つの絞り込み要素のどちらかが正しいことを表す絞り込み条件。

        :param left: 絞り込み要素 1
        :param right: 絞り込み要素 2
        :return: 絞り込み条件オブジェクト
        """
        return JsonFilterOperator._binary("or", left, right)

    @staticmethod
    def and_(
        left: "JsonFilterOperator", right: "JsonFilterOperator"
    ) -> "JsonFilterOperator":
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
    def set_range(
        field_type: FieldType,
        from_: Optional[Union[int, datetime]] = None,
        to_: Optional[Union[int, datetime]] = None,
        include_lower: bool = True,
        include_upper: bool = True,
    ) -> "JsonFilterTerm":
        """
        検索フィールドについて、与えられた数値または日付の範囲内かを調べる検索要素。

        :param field_type: 検索するフィールド
        :param from_: 数値の下限または投稿時刻の最古
        :param to_: 数値の上限または投稿時刻の最新
        :param include_lower: from_ を含むかどうか
        :param include_upper: to_ を含むかどうか
        :return: 絞り込み要素オブジェクト
        """
        term: JsonFilterTerm = JsonFilterTerm()
        if from_ is None and to_ is None:
            raise Exception("上限も下限も指定されていません")
        json_: Dict[str, Union[str, bool, int]] = {
            "type": "range",
            "field": field_type.value,
        }

        match field_type:
            case (
                FieldType.USER_ID
                | FieldType.CHANNEL_ID
                | FieldType.VIEW_COUNTER
                | FieldType.MYLIST_COUNTER
                | FieldType.LIKE_COUNTER
                | FieldType.LENGTH_SECONDS
                | FieldType.COMMENT_COUNTER
            ):
                if from_ is not None:
                    json_["from"] = JsonFilterTerm._arrange_value(
                        from_, int, field_type
                    )
                if to_ is not None:
                    json_["to"] = JsonFilterTerm._arrange_value(to_, int, field_type)
            case (FieldType.START_TIME | FieldType.LAST_COMMENT_TIME):
                if from_ is not None:
                    json_["from"] = JsonFilterTerm._arrange_value(
                        from_, datetime, field_type
                    )

                if to_ is not None:
                    json_["to"] = JsonFilterTerm._arrange_value(
                        to_, datetime, field_type
                    )
            case _:
                raise TypeError(f"{field_type.value}はjson_filterに指定できないフィールドです")
        if include_lower:
            json_["include_lower"] = include_lower
        if include_upper:
            json_["include_upper"] = include_upper
        term.json = json_
        return term

    @staticmethod
    def _arrange_value(
        value: Union[int, datetime],
        type_: Union[Type[int], Type[datetime]],
        field_type: FieldType,
    ) -> Union[int, str]:
        if type(value) is type_:
            if type_ is int:
                return value
            elif type_ is datetime:
                return value.strftime("%Y-%m-%dT%H:%M:%S+09:00")
        else:
            raise TypeError(f"フィールド {field_type.value} には {type_} が指定されるべきです")
