import urllib.parse
from json import JSONEncoder
from typing import Dict, Union

from nicovideo_api_client.api.v2.complex_filter import ComplexFilterOperator, ComplexFilterTerm
from nicovideo_api_client.api.v2.limit import SnapshotSearchAPIV2Limit
from nicovideo_api_client.api.v2.simple_filter import SnapshotSearchAPIV2SimpleFilter


class SnapshotSearchAPIV2Filter:
    def __init__(self, query: Dict[str, str]):
        self.query: Dict[str, str] = query

    def simple_filter(self) -> SnapshotSearchAPIV2SimpleFilter:
        return SnapshotSearchAPIV2SimpleFilter(self.query)

    def complex_filter(
            self,
            op: Union[ComplexFilterOperator, ComplexFilterTerm]
    ) -> SnapshotSearchAPIV2Limit:
        self.query["jsonFilter"] = urllib.parse.quote_plus(JSONEncoder().encode(op.json))
        return SnapshotSearchAPIV2Limit(self.query)
