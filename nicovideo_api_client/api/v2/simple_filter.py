import re
from datetime import datetime
from typing import Dict, Optional, Union

from nicovideo_api_client.api.v2.limit import SnapshotSearchAPIV2Limit
from nicovideo_api_client.constants import (
    CombinedDict,
    FieldType,
    MatchDict,
    MatchValue,
    RangeDict,
    RangeValue,
)


class SnapshotSearchAPIV2SimpleFilter:
    def __init__(self, query: Dict[str, str]):
        self._query: Dict[str, str] = query

    def _cast_value(
        self, field_type: FieldType, value: Union[int, str, datetime]
    ) -> str:
        match field_type:
            case (
                FieldType.START_TIME
                | FieldType.LAST_COMMENT_TIME
                | FieldType.START_TIME
            ):
                if not isinstance(value, datetime):
                    raise TypeError(
                        f"FieldType.{field_type.value}を指定した時の型は datetime であるべきです"
                    )
                v = value.strftime("%Y-%m-%dT%H:%M:%S+09:00")
            case FieldType.CONTENT_ID:
                if isinstance(value, int):
                    v = f"sm{value}"
                elif isinstance(value, str):
                    if not re.compile(r"sm\d+").fullmatch(value):
                        raise TypeError("FieldType.CONTENT_IDはsm(数字)の形で表されるべきです")
                    v = value
                else:
                    raise TypeError("FieldType.CONTENT_IDを指定した時の型は int または str であるべきです")
            case (
                FieldType.COMMENT_COUNTER
                | FieldType.LENGTH_SECONDS
                | FieldType.LIKE_COUNTER
                | FieldType.MYLIST_COUNTER
                | FieldType.VIEW_COUNTER
            ):
                if isinstance(value, int):
                    v = value
                elif isinstance(value, str):
                    if not isinstance(int(value), int):
                        raise TypeError(f"FieldType.{field_type.value}は整数が指定されるべきです")
                    v = int(value)
                else:
                    raise TypeError(
                        f"FieldType.{field_type.value}を指定した時の型は int または str であるべきです"
                    )
            case (
                FieldType.GENRE_KEYWORD
                | FieldType.GENRE
                | FieldType.TAGS_EXACT
                | FieldType.TAGS
                | FieldType.CATEGORY_TAGS
            ):
                if not isinstance(value, str):
                    raise TypeError(
                        f"FieldType.{field_type.value}を指定した時の型は str であるべきです"
                    )
                v = value
            case (
                FieldType.TITLE
                | FieldType.DESCRIPTION
                | FieldType.USER_ID
                | FieldType.CHANNEL_ID
                | FieldType.THUMBNAIL_URL
                | FieldType.LAST_RES_BODY
            ):
                raise TypeError(
                    f"FieldType.{field_type.value}はfilterに指定できないFieldTypeです"
                )
            case _:
                raise NotImplementedError("未知のTypeが指定されました")
        return v

    def _match_filter(self, field_type: FieldType, match_value: MatchValue):
        field_count: int = 0
        for value in match_value:
            v = self._cast_value(field_type, value)

            self._query[f"filters[{field_type.value}][{field_count}]"] = v
            field_count += 1
        return self

    def _range_filter(self, field_type: FieldType, range_value: RangeValue):
        for literal, value in range_value.items():
            v = self._cast_value(field_type, value)

            self._query[f"filters[{field_type.value}][{literal}]"] = v
        return self

    def _classify(self, field_type: FieldType, value: Union[MatchValue, RangeValue]):
        if type(value) is list:
            self._match_filter(field_type, value)
        elif type(value) is dict:
            self._range_filter(field_type, value)
        else:
            raise TypeError("検索する値はListまたはDictで渡されるべきです")
        return self

    def filter(
        self,
        value: Optional[Union[MatchDict, RangeDict, CombinedDict]] = None,
        combine: bool = False,
    ) -> SnapshotSearchAPIV2Limit:
        """
        検索フィルターを指定する。

        Args:
            value(Optional[Union[MatchDict, RangeDict, CombinedDict]]):
                フィルターを指定したいフィールドの辞書
            combine(bool):
                複合検索を使用する場合にTrueを指定する。デフォルト値はFalse

        Returns:
            レスポンス要素数の指定オブジェクト

        Examples:
            #一致検索の場合: filter(MatchDict型の辞書, False)
            #範囲検索の場合: filter(RangeDict型の辞書, False)
            #複合検索の場合: filter(CombinedDict型の辞書, True)
        """
        if self._query["q"] == "" and value is None:
            raise Exception("キーワード無し検索を行う場合には必ず検索フィルタを指定してください")
        elif value is not None:
            if type(value) is not dict:
                raise TypeError("検索にはMatchDictまたはRangeDictどちらかの型を指定する必要があります")
            elif combine is True:
                field_type_list: list = []
                for k, v in value.items():
                    if k in field_type_list:
                        raise Exception("複合検索では同じFieldTypeを複数回指定することはできません")
                    field_type_list.append(k)
                    self._classify(k, v)
            else:
                for k, v in value.items():
                    self._classify(k, v)
        return SnapshotSearchAPIV2Limit(self._query)
