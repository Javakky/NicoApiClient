from datetime import datetime
from typing import Dict, List, Union

from nicovideo_api_client.constants import FieldType


class FilterBuilder:
    def __init__(self, filter: Dict[str, Union[Dict[str, Union[str, int, datetime]], Union[List[str], List[int], List[datetime]]]] = {}):
        self.filter: Dict[str, Union[Dict[str, Union[str, int, datetime]], Union[List[str], List[int], List[datetime]]]] = filter

    def __cast_literal(self, literal: str) -> str:
        if literal != "gt" and literal != "gte" and literal != "lt" and literal != "lte":
            match literal:
                case ">":
                    literal = "gt"
                case ">=":
                    literal = "gte"
                case "<":
                    literal = "lt"
                case "<=":
                    literal = "lte"
                case _:
                    raise ValueError("未知のリテラルが指定されました")
        return literal

    def range_filter(
        self,
        field_type: FieldType = None,
        literal1: str = None,
        value1: Union[str, int, datetime] = None,
        literal2: str = None,
        value2: Union[str, int, datetime] = None,
    ) -> "FilterBuilder":
        """
        範囲検索用の辞書を組み立てる

        Args:
            field_type(FieldType):
                フィルターを指定したいフィールド
            literal1(str):
                フィルター指定範囲
            value1(Union[str, int, datetime]):
                フィルターの値
            literal2(str):
                フィルター指定範囲2
            value2(Union[str, int, datetime]):
                フィルターの値2

        Returns:
            フィルター辞書組み立てオブジェクト
        """
        if field_type is not None and literal1 is not None and value1 is not None:
            if literal2 is not None and value2 is not None:
                self.filter[field_type.value] = {self.__cast_literal(literal1): value1, self.__cast_literal(literal2): value2}
            else:
                self.filter[field_type.value] = {self.__cast_literal(literal1): value1}

        return self

    def match_filter(self, field_type: FieldType = None, value: Union[List[str], List[int], List[datetime]] = None) -> "FilterBuilder":
        """
        一致検索用の辞書を組み立てる

        Args:
            field_type(FieldType):
                フィルターを指定したいフィールド
            value(Union[List[str], List[int], List[datetime]]):
                フィルターに指定するの値のリスト

        Returns:
            フィルター辞書組み立てオブジェクト
        """
        if field_type is not None and value is not None:
            self.filter[field_type.value] = value

        return self
