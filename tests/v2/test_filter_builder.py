import unittest

from nicovideo_api_client.api.v2.filter_builder import FilterBuilder
from nicovideo_api_client.constants import FieldType


class FilterBuilderTestCase(unittest.TestCase):
    @staticmethod
    def test_filter_nothing():
        actual = FilterBuilder({}).match_filter().range_filter()
        print(actual.filter)
        assert actual.filter == {}

    @staticmethod
    def test_match_filter():
        actual = FilterBuilder({}).match_filter(FieldType.TITLE, ["初音ミク"])
        assert actual.filter == {"title": ["初音ミク"]}

    @staticmethod
    def test_range_filter():
        actual = FilterBuilder({}).range_filter(FieldType.VIEW_COUNTER, "gt", 1000)
        assert actual.filter == {"viewCounter": {"gt": 1000}}

    @staticmethod
    def test_range_filter_set():
        actual = FilterBuilder({}).range_filter(FieldType.VIEW_COUNTER, "gt", 1000, "lte", 5000)
        assert actual.filter == {"viewCounter": {"gt": 1000, "lte": 5000}}

    @staticmethod
    def test_range_filter_sign():
        actual = FilterBuilder({}).range_filter(FieldType.VIEW_COUNTER, ">", 1000, "<=", 5000)
        assert actual.filter == {"viewCounter": {"gt": 1000, "lte": 5000}}

    @staticmethod
    def test_combine_filter():
        actual = (
            FilterBuilder({}).match_filter(FieldType.TITLE, ["初音ミク"]).range_filter(FieldType.VIEW_COUNTER, "gt", 1000)
        )
        assert actual.filter == {"title": ["初音ミク"], "viewCounter": {"gt": 1000}}


if __name__ == "__main__":
    unittest.main()
