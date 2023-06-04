import unittest

from nicovideo_api_client.api.v2.filter_builder import FilterBuilder
from nicovideo_api_client.constants import FieldType


class FilterBuilderTestCase(unittest.TestCase):
    @staticmethod
    def test_filter_nothing():
        assert FilterBuilder().match_filter().range_filter() == {}

    @staticmethod
    def test_match_filter():
        assert FilterBuilder().match_filter(FieldType.TITLE, "初音ミク") == {"title": "初音ミク"}

    @staticmethod
    def test_range_filter():
        assert FilterBuilder().range_filter(FieldType.VIEW_COUNTER, "gt", 1000) == {"viewCounter": {"gt": 1000}}

    @staticmethod
    def test_range_filter_set():
        assert FilterBuilder().range_filter(FieldType.VIEW_COUNTER, "gt", 1000, "lte", 5000) == {
            "viewCounter": {"gt": 1000, "lte": 5000}
        }

    @staticmethod
    def test_range_filter_sign():
        assert FilterBuilder().range_filter(FieldType.VIEW_COUNTER, ">", 1000, "<=", 5000) == {
            "viewCounter": {"gt", 1000, "lte", 5000}
        }


if __name__ == "__main__":
    unittest.main()
