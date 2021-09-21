import unittest
from datetime import datetime

from nicovideo_api_client.api.v2.json_filter import JsonFilterOperator, JsonFilterTerm
from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import FieldType


class SnapshotSearchAPIV2RequestTestCase(unittest.TestCase):
    def test_build_url(self):
        actual = SnapshotSearchAPIV2() \
            .targets({FieldType.TITLE}) \
            .query("歌ってみた") \
            .field({FieldType.TITLE}) \
            .sort(FieldType.VIEW_COUNTER) \
            .simple_filter().filter() \
            .limit(10)
        assert actual.build_url(False) == "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search" \
                                          "?targets=title&q=%E6%AD%8C%E3%81%A3%E3%81%A6%E3%81%BF%E3%81%9F&fields" \
                                          "=title&_sort=-viewCounter"

    def test_build_url_jsonFilter(self):
        actual = SnapshotSearchAPIV2() \
            .targets({FieldType.TITLE}) \
            .query("歌ってみた") \
            .field({FieldType.TITLE}) \
            .sort(FieldType.VIEW_COUNTER) \
            .json_filter(
            JsonFilterOperator.not_(
                JsonFilterTerm.set_range_time(
                    to_=datetime(2021, 1, 1, 0, 0, 0),
                    include_upper=False
                )
            )
        ).limit(10)
        assert actual.build_url(True) == "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search" \
                                         "?targets=title&q=歌ってみた&fields=title&_sort=-viewCounter&jsonFilter=%7B" \
                                         "%22type%22%3A+%22not%22%2C+%22filter%22%3A+%7B%22type%22%3A+%22range%22%2C" \
                                         "+%22field%22%3A+%22startTime%22%2C+%22to%22%3A+%222021-01-01T00%3A00%3A00" \
                                         "%2B09%3A00%22%2C+%22include_lower%22%3A+true%7D%7D"


if __name__ == '__main__':
    unittest.main()
