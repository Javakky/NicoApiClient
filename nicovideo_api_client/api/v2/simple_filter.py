import re
from datetime import datetime
from typing import Dict, List, Union

from nicovideo_api_client.api.v2.limit import SnapshotSearchAPIV2Limit
from nicovideo_api_client.constants import FieldType


class SnapshotSearchAPIV2SimpleFilter:
    def __init__(self, query: Dict[str, str]):
        self._query: Dict[str, str] = query
        self._filters: Dict[str, List[str]] = {}

    def set_filter(self, field_type: FieldType, value: Union[int, str, datetime]):
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
        else:
            raise NotImplementedError("未知のTypeが指定されました")

        if field_type.value not in self._filters:
            self._filters[field_type.value] = []

        self._filters[field_type.value].append(v)
        return v

    def matchFilter(self, field_type: FieldType, value: Union[int, str, datetime]):
        v = self.set_filter(field_type, value)

        self._query[
            f"filters[{field_type.value}][{len(self._filters[field_type.value])}]"
        ] = v
        return self

    def rangeFilter(
        self, field_type: FieldType, value: Union[int, str, datetime], range: str
    ):
        v = self.set_filter(field_type, value)

        self._query[f"filters[{field_type.value}][{range}]"] = v
        return self

    def filter(self, value: Union[list, dict] = []) -> SnapshotSearchAPIV2Limit:
        if isinstance(value, list):
            for v in value:
                if len(v) != 2:
                    raise Exception("一致検索には検索する値と型を指定するべきです。")
                self.matchFilter(v[0], v[1])
        elif isinstance(value, dict):
            for k, v in value.items():
                if len(v) != 2:
                    raise Exception(
                        "範囲検索のvalueはFeildTypeと[gt, lt, gte, lte]のいずれかをとるべきです。"
                    )
                self.rangeFilter(k, v[0], v[1])
        else:
            raise Exception("検索にはリストか辞書を渡す必要があります。")
        return SnapshotSearchAPIV2Limit(self._query)
