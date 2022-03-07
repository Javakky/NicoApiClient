import unittest
from datetime import datetime, timedelta
from unittest import mock

from nicovideo_api_client.api.v2.json_filter import JsonFilterOperator, JsonFilterTerm
from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import CombinedDict, FieldType, MatchDict, MatchValue, RangeDict, RangeValue
from tests.mock_response import MockResponse

META_DATA = {
    "status": 200,
    "totalCount": 1,
    "id": "594513df-85ea-4122-9859-f4ec2701cacf",
}

DATA_DATA = {
    "contentId": "sm9",
    "title": "テスト",
    "description": "テスト",
    "startTime": "2016-11-03T02:09:11+09:00",
    "viewCounter": 1,
}

META_DATA_MUL = {
    "status": 200,
    "totalCount": 101,
    "id": "594513df-85ea-4122-9859-f4ec2701cacf",
}


class SnapshotSearchAPIV2RequestTestCase(unittest.TestCase):
    @staticmethod
    def test_build_url():
        """検索フィルターなし"""
        actual = (
            SnapshotSearchAPIV2()
            .targets({FieldType.TITLE})
            .single_query("テスト")
            .field({FieldType.TITLE})
            .sort(FieldType.VIEW_COUNTER)
            .simple_filter()
            .filter()
            .limit(10)
            .user_agent("NicoApiClient", "0.5.0")
        )
        assert (
            actual.build_url(False) == "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
            "?targets=title&q=%E3%83%86%E3%82%B9%E3%83%88&fields"
            "=title&_sort=-viewCounter"
        )

    @staticmethod
    def test_build_url_query():
        actual = (
            SnapshotSearchAPIV2()
            .targets({FieldType.TITLE})
            .query(["歌ってみた"])
            .and_(["初音ミク", "鏡音リン"])
            .field({FieldType.TITLE})
            .sort(FieldType.VIEW_COUNTER)
            .simple_filter()
            .filter()
            .limit(10)
            .user_agent("NicoApiClient", "0.5.0")
        )

        assert (
            actual.build_url(False) == "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
            "?targets=title&q=%E6%AD%8C%E3%81%A3%E3%81%A6%E3%81%BF%E3%81%9F+"
            "%E5%88%9D%E9%9F%B3%E3%83%9F%E3%82%AF+OR+"
            "%E9%8F%A1%E9%9F%B3%E3%83%AA%E3%83%B3&"
            "fields=title&_sort=-viewCounter"
        )

    @staticmethod
    def test_build_url_single_query():
        actual = (
            SnapshotSearchAPIV2()
            .targets({FieldType.TITLE})
            .single_query("歌ってみた OR 踊ってみた")
            .field({FieldType.TITLE})
            .sort(FieldType.VIEW_COUNTER)
            .simple_filter()
            .filter()
            .limit(10)
            .user_agent("NicoApiClient", "0.5.0")
        )

        assert (
            actual.build_url(False) == "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
            "?targets=title&q=%E6%AD%8C%E3%81%A3%E3%81%A6%E3%81%BF%E3%81%9F"
            "+OR+%E8%B8%8A%E3%81%A3%E3%81%A6%E3%81%BF%E3%81%9F&fields=title&"
            "_sort=-viewCounter"
        )

    @staticmethod
    def test_build_url_match_filter():
        # フィルタの指定
        view: MatchValue = [100, 1000, 10000]
        mylist: MatchValue = [10, 100]
        match_filter: MatchDict = {
            FieldType.VIEW_COUNTER: view,
            FieldType.MYLIST_COUNTER: mylist,
        }
        actual = (
            SnapshotSearchAPIV2()
            .targets({FieldType.TITLE})
            .single_query("歌ってみた")
            .field(
                {
                    FieldType.TITLE,
                    FieldType.DESCRIPTION,
                    FieldType.VIEW_COUNTER,
                    FieldType.MYLIST_COUNTER,
                }
            )
            .sort(FieldType.VIEW_COUNTER)
            .simple_filter()
            .filter(match_filter)
            .limit(10)
            .user_agent("NicoApiClient", "0.5.0")
        )
        assert (
            actual.build_url(False) == "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
            "?targets=title&q=%E6%AD%8C%E3%81%A3%E3%81%A6%E3%81%BF%E3%81%9F&"
            "fields=description%2CmylistCounter%2Ctitle%2CviewCounter&"
            "_sort=-viewCounter&filters%5BviewCounter%5D%5B0%5D=100&"
            "filters%5BviewCounter%5D%5B1%5D=1000&"
            "filters%5BviewCounter%5D%5B2%5D=10000&"
            "filters%5BmylistCounter%5D%5B0%5D=10&"
            "filters%5BmylistCounter%5D%5B1%5D=100"
        )

    @staticmethod
    def test_build_url_range_filter():
        # フィルタの指定
        view: RangeValue = {"gte": 1000, "lt": 10000}
        mylist: RangeValue = {"gt": 10, "lte": 100}
        range_filter: RangeDict = {
            FieldType.VIEW_COUNTER: view,
            FieldType.MYLIST_COUNTER: mylist,
        }

        actual = (
            SnapshotSearchAPIV2()
            .targets({FieldType.TITLE})
            .single_query("歌ってみた")
            .field(
                {
                    FieldType.TITLE,
                    FieldType.DESCRIPTION,
                    FieldType.VIEW_COUNTER,
                    FieldType.MYLIST_COUNTER,
                }
            )
            .sort(FieldType.VIEW_COUNTER)
            .simple_filter()
            .filter(range_filter)
            .limit(10)
            .user_agent("NicoApiClient", "0.5.0")
        )
        assert (
            actual.build_url(False) == "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
            "?targets=title&q=%E6%AD%8C%E3%81%A3%E3%81%A6%E3%81%BF%E3%81%9F&"
            "fields=description%2CmylistCounter%2Ctitle%2CviewCounter&"
            "_sort=-viewCounter&filters%5BviewCounter%5D%5Bgte%5D=1000&"
            "filters%5BviewCounter%5D%5Blt%5D=10000&"
            "filters%5BmylistCounter%5D%5Bgt%5D=10&"
            "filters%5BmylistCounter%5D%5Blte%5D=100"
        )

    @staticmethod
    def test_url_builder_combi_filter():
        # フィルタの指定
        view: MatchValue = [1000, 10000]
        mylist: RangeValue = {"gt": 10, "lte": 100}
        combined_filter: CombinedDict = {
            FieldType.VIEW_COUNTER: view,
            FieldType.MYLIST_COUNTER: mylist,
        }
        combine: bool = True

        actual = (
            SnapshotSearchAPIV2()
            .targets({FieldType.TITLE})
            .single_query("歌ってみた")
            .field(
                {
                    FieldType.TITLE,
                    FieldType.DESCRIPTION,
                    FieldType.VIEW_COUNTER,
                    FieldType.MYLIST_COUNTER,
                }
            )
            .sort(FieldType.VIEW_COUNTER)
            .simple_filter()
            .filter(combined_filter, combine)
            .limit(10)
            .user_agent("NicoApiClient", "0.5.0")
        )
        assert (
            actual.build_url(False) == "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
            "?targets=title&q=%E6%AD%8C%E3%81%A3%E3%81%A6%E3%81%BF%E3%81%9F&"
            "fields=description%2CmylistCounter%2Ctitle%2CviewCounter&"
            "_sort=-viewCounter&filters%5BviewCounter%5D%5B0%5D=1000&"
            "filters%5BviewCounter%5D%5B1%5D=10000&"
            "filters%5BmylistCounter%5D%5Bgt%5D=10&"
            "filters%5BmylistCounter%5D%5Blte%5D=100"
        )

    @staticmethod
    def test_build_url_jsonFilter():
        actual = (
            SnapshotSearchAPIV2()
            .targets({FieldType.TITLE})
            .single_query("テスト")
            .field({FieldType.TITLE})
            .sort(FieldType.VIEW_COUNTER)
            .json_filter(
                JsonFilterOperator.not_(
                    JsonFilterTerm.set_range(
                        FieldType.START_TIME,
                        to_=datetime(2021, 1, 1, 0, 0, 0),
                        include_upper=False,
                    )
                )
            )
            .limit(10)
            .user_agent("NicoApiClient", "0.5.0")
        )
        assert (
            actual.build_url(True) == "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
            "?targets=title&q=テスト&fields=title&_sort=-viewCounter&jsonFilter=%7B"
            "%22type%22%3A+%22not%22%2C+%22filter%22%3A+%7B%22type%22%3A+%22range%22%2C"
            "+%22field%22%3A+%22startTime%22%2C+%22to%22%3A+%222021-01-01T00%3A00%3A00"
            "%2B09%3A00%22%2C+%22include_lower%22%3A+true%7D%7D"
        )

    @staticmethod
    def mocked_requests_get_success_single_result(*_, **__):
        return MockResponse(
            {
                "meta": META_DATA,
                "data": [DATA_DATA],
            },
            200,
            timedelta(milliseconds=300),
        )

    @staticmethod
    @mock.patch("requests.get", side_effect=mocked_requests_get_success_single_result)
    def test_request(_):
        actual = (
            SnapshotSearchAPIV2()
            .targets({FieldType.TITLE})
            .single_query("テスト")
            .field({FieldType.TITLE})
            .sort(FieldType.VIEW_COUNTER)
            .simple_filter()
            .filter()
            .limit(10)
            .user_agent("NicoApiClient", "0.5.0")
            .request()
        )
        assert actual.meta_id() == [META_DATA["id"]]
        assert actual.status() == [META_DATA["status"]]
        assert actual.total_count() == META_DATA["totalCount"]
        assert len(actual.data()) == 1

        assert actual.data()[0]["contentId"] == DATA_DATA["contentId"]
        assert actual.data()[0]["title"] == DATA_DATA["title"]
        assert actual.data()[0]["description"] == DATA_DATA["description"]
        assert actual.data()[0]["startTime"] == DATA_DATA["startTime"]
        assert actual.data()[0]["viewCounter"] == DATA_DATA["viewCounter"]

    @staticmethod
    def mocked_requests_get_success_multiple_result(*args, **__):
        return MockResponse(
            {
                "meta": META_DATA_MUL,
                "data": [DATA_DATA for _ in range(100 if "_offset" in args[0] else 1)],
            },
            200,
            timedelta(milliseconds=300),
        )

    @staticmethod
    @mock.patch("requests.get", side_effect=mocked_requests_get_success_multiple_result)
    def test_multiple_request(_):
        actual = (
            SnapshotSearchAPIV2()
            .targets({FieldType.TITLE})
            .query("テスト")
            .field({FieldType.TITLE})
            .sort(FieldType.VIEW_COUNTER)
            .simple_filter()
            .filter()
            .limit(200)
            .user_agent("NicoApiClient", "0.5.0")
            .request()
        )
        assert actual.meta_id() == [META_DATA_MUL["id"], META_DATA_MUL["id"]]
        assert actual.status() == [META_DATA_MUL["status"], META_DATA_MUL["status"]]
        assert actual.total_count() == META_DATA_MUL["totalCount"]
        assert len(actual.data()) == 101

        assert actual.data()[0]["contentId"] == DATA_DATA["contentId"]
        assert actual.data()[0]["title"] == DATA_DATA["title"]
        assert actual.data()[0]["description"] == DATA_DATA["description"]
        assert actual.data()[0]["startTime"] == DATA_DATA["startTime"]
        assert actual.data()[0]["viewCounter"] == DATA_DATA["viewCounter"]

        assert actual.data()[100]["contentId"] == DATA_DATA["contentId"]
        assert actual.data()[100]["title"] == DATA_DATA["title"]
        assert actual.data()[100]["description"] == DATA_DATA["description"]
        assert actual.data()[100]["startTime"] == DATA_DATA["startTime"]
        assert actual.data()[100]["viewCounter"] == DATA_DATA["viewCounter"]


if __name__ == "__main__":
    unittest.main()
