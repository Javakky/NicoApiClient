from datetime import datetime
from typing import Dict, List, Any

from nicovideo_api_client.nicovideo.constants import FieldType
from nicovideo_api_client.nicovideo.api.v2.limit import SnapshotSearchAPIV2Limit

import re


class SnapshotSearchAPIV2SimpleFilter:
    def __init__(self, query: Dict[str, str]):
        self.query: Dict[str, str] = query
        self.filters: Dict[str, List[Any]] = {}

    def set_filter(self, type: FieldType, value: Any):
        if type == FieldType.START_TIME:
            if not isinstance(value, datetime):
                raise TypeError("FieldType.START_TIMEを指定した時の型は datetime であるべきです")
            v = value.strftime('%Y-%m-%dT%H:%M:%S+09:00')
        elif type == FieldType.CONTENT_ID:
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

        if type.value not in self.filters:
            self.filters[type.value] = []

        self.filters[type.value].append(v)

        self.query[
            f'filters[{type.value}][{len(self.filters[type.value])}]'
        ] = v
        return self

    def filter(self) -> SnapshotSearchAPIV2Limit:
        return SnapshotSearchAPIV2Limit(self.query)