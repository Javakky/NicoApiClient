from datetime import datetime
from typing import Dict, Union

from nicovideo_api_client.constants import FieldType


class FilterBuilder:
    def __init__(self, filter: Dict[str, str] = {}):
        self.filter: Dict[str, str] = filter

    def _cast_literal(self, literal: str) -> str:
        if literal == "gt" or literal == "gte" or literal == "lt" or literal == "lte":
            l = literal
        else:
            match literal:
                case ">":
                    l = "gt"
                case ">=":
                    l = "gte"
                case "<":
                    l = "lt"
                case "<=":
                    l = "lte"
                case _:
                    raise ValueError("未知のリテラルが指定されました")
        return l

    def range_filter(
            self, 
            field_type: FieldType, 
            literal1: str, 
            value1: Union[str, int, datetime], 
            literal2: str = None, 
            value2: Union[str, int, datetime] = None
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
        if literal2 is not None:
            if value2 is None:
                raise ValueError("値が指定されていません")
            self.filter[field_type] = {self._cast_literal(literal1): value1, self._cast_literal(literal2): value2}
        else:
            self.filter[field_type] = {self._cast_literal(literal1): value1}        
        
        return self


    def match_filter(
            self, 
            field_type: FieldType, 
            value: Union[str, int, datetime]
    ) -> "FilterBuilder":
        """
        一致検索用の辞書を組み立てる

        Args:
            field_type(FieldType):
                フィルターを指定したいフィールド
            value(Union[str, int, datetime]):
                フィルターの値
        
        Returns:
            フィルター辞書組み立てオブジェクト
        """
        self.filter[field_type] = value

        return self