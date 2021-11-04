import re
from datetime import datetime
from typing import List, Dict, Union, Optional

from nicovideo_api_client.api.v2.limit import SnapshotSearchAPIV2Limit
from nicovideo_api_client.constants import (
    FieldType,
    MatchValue,
    RangeValue,
    MatchDict,
    RangeDict,
)


class SnapshotSearchAPIV2SimpleFilter:
    def __init__(self, query: Dict[str, str]):
        self._query: Dict[str, str] = query

    def _cast_value(
        self, field_type: FieldType, value: Union[int, str, datetime]
    ) -> str:
        if field_type == FieldType.START_TIME:
            if not isinstance(value, datetime):
                raise TypeError("FieldType.START_TIMEを指定した時の型は datetime であるべきです")
            v = value.strftime("%Y-%m-%dT%H:%M:%S+09:00")
        elif field_type == FieldType.CONTENT_ID:
            if isinstance(value, int):
                v = f"sm{value}"
            elif isinstance(value, str):
                if not re.compile(r"sm\d+").fullmatch(value):
                    raise TypeError("FieldType.CONTENT_IDはsm(数字)の形で表されるべきです")
                v = value
            else:
                raise TypeError("FieldType.CONTENT_IDを指定した時の型は int または str であるべきです")
        elif field_type == FieldType.VIEW_COUNTER:
            if isinstance(value, int):
                v = value
            elif isinstance(value, str):
                if not isinstance(int(value), int):
                    raise TypeError("FieldType.VIEW_COUNTERは整数が指定されるべきです")
                v = int(value)
            else:
                raise TypeError("FieldType.VIEW_COUNTERを指定した時の型は int または str であるべきです")
        elif field_type == FieldType.MYLIST_COUNTER:
            if isinstance(value, int):
                v = value
            elif isinstance(value, str):
                if not isinstance(int(value), int):
                    raise TypeError("FieldType.MYLIST_COUNTERは整数が指定されるべきです")
                v = int(value)
            else:
                raise TypeError("FieldType.MYLIST_COUNTERを指定した時の型は int または str であるべきです")
        elif field_type == FieldType.LIKE_COUNTER:
            if isinstance(value, int):
                v = value
            elif isinstance(value, str):
                if not isinstance(int(value), int):
                    raise TypeError("FieldType.LIKE_COUNTERは整数が指定されるべきです")
                v = int(value)
            else:
                raise TypeError("FieldType.LIKE_COUNTERを指定した時の型は int または str であるべきです")
        elif field_type == FieldType.LENGTH_SECONDS:
            if isinstance(value, int):
                v = value
            elif isinstance(value, str):
                if not isinstance(int(value), int):
                    raise TypeError("FieldType.LENGTH_SECONDSは整数が指定されるべきです")
                v = int(value)
            else:
                raise TypeError("FieldType.LENGTH_SECONDSを指定した時の型は int または str であるべきです")
        elif field_type == FieldType.START_TIME:
            if not isinstance(value, datetime):
                raise TypeError("FieldType.START_TIMEを指定した時の型は datetime であるべきです")
            v = value.strftime("%Y-%m-%dT%H:%M:%S+09:00")
        elif field_type == FieldType.COMMENT_COUNTER:
            if isinstance(value, int):
                v = value
            elif isinstance(value, str):
                if not isinstance(int(value), int):
                    raise TypeError("FieldType.COMMENT_COUNTERは整数が指定されるべきです")
                v = int(value)
            else:
                raise TypeError(
                    "FieldType.COMMENT_COUNTERを指定した時の型は int または str であるべきです"
                )
        elif field_type == FieldType.LAST_COMMENT_TIME:
            if not isinstance(value, datetime):
                raise TypeError("FieldType.LAST_COMMENT_TIMEを指定した時の型は datetime であるべきです")
            v = value.strftime("%Y-%m-%dT%H:%M:%S+09:00")
        elif field_type == FieldType.CATEGORY_TAGS:
            if not isinstance(value, str):
                raise TypeError("FieldType.CATEGORY_TAGSを指定した時の型は str であるべきです")
            v = value
        elif field_type == FieldType.TAGS:
            if not isinstance(value, str):
                raise TypeError("FieldType.TAGSを指定した時の型は str であるべきです")
            v = value
        elif field_type == FieldType.TAGS_EXACT:
            if not isinstance(value, str):
                raise TypeError("FieldType.TAGS_EXACTを指定した時の型は str であるべきです")
            v = value
        elif field_type == FieldType.GENRE:
            if not isinstance(value, str):
                raise TypeError("FieldType.GENREを指定した時の型は str であるべきです")
            v = value
        elif field_type == FieldType.GENRE_KEYWORD:
            if not isinstance(value, str):
                raise TypeError("FieldType.GENRE_KEYWORDを指定した時の型は str であるべきです")
            v = value
        elif (
            field_type == FieldType.TITLE
            or field_type == FieldType.DESCRIPTION
            or field_type == FieldType.USER_ID
            or field_type == FieldType.CHANNEL_ID
            or field_type == FieldType.THUMBNAIL_URL
            or field_type == FieldType.LAST_RES_BODY
        ):
            raise TypeError("filterに指定できないFieldTypeです")
        else:
            raise NotImplementedError("未知のTypeが指定されました")

        return v

    def _match_filter(self, field_type: FieldType, match_value: MatchValue):
        field_count: int = 0
        for value in match_value:
            v = self._cast_value(field_type, value)

            self._query[f"filters[{field_type}][{field_count}]"] = v
            field_count += 1
        return self

    def _range_filter(self, field_type: FieldType, range_value: RangeValue):
        for literal, value in range_value.items():
            v = self._cast_value(field_type, value)

            self._query[f"filters[{field_type}][{literal}]"] = v
        return self

    def filter(
        self, value: Optional[Union[MatchDict, RangeDict]] = None
    ) -> SnapshotSearchAPIV2Limit:
        if value is not None:
            if type(value) is dict:
                for k, v in value.items():
                    if type(v) is list:
                        self._match_filter(k, v)
                    elif type(v) is dict:
                        self._range_filter(k, v)
                    else:
                        raise TypeError("検索する値はListまたはDictで渡されるべきです")
            else:
                raise TypeError("検索にはMatchDictまたはRangeDictどちらかの型を指定する必要があります")
        return SnapshotSearchAPIV2Limit(self._query)
