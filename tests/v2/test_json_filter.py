import unittest
from datetime import datetime

from nicovideo_api_client.api.v2.filter import SnapshotSearchAPIV2Filter
from nicovideo_api_client.api.v2.json_filter import JsonFilterTerm, JsonFilterOperator


class JsonFilterTestCase(unittest.TestCase):
    term_time = JsonFilterTerm.set_range_time(
        from_=datetime(2021, 1, 1),
        to_=datetime(2021, 12, 31),
        include_upper=True,
        include_lower=True,
    )

    term_view = JsonFilterTerm.set_range_view(
        from_=100, to_=1000, include_upper=True, include_lower=True
    )

    def test_set_range_time(self):
        actual = SnapshotSearchAPIV2Filter({"q": "test"}).json_filter(self.term_time)
        assert (
            actual._query["jsonFilter"]
            == "%7B%22type%22%3A+%22range%22%2C+%22field%22%3A+%22startTime%22%2C"
            "+%22from%22%3A+%222021-01-01T00%3A00%3A00%2B09%3A00%22%2C+%22to%22%3A"
            "+%222021-12-31T00%3A00%3A00%2B09%3A00%22%2C+%22include_lower%22%3A"
            "+true%2C+%22include_upper%22%3A+true%7D"
        )

    def test_set_range_view(self):
        actual = SnapshotSearchAPIV2Filter({"q": "test"}).json_filter(self.term_view)
        assert (
            actual._query["jsonFilter"]
            == "%7B%22type%22%3A+%22range%22%2C+%22field%22%3A+%22viewCounter%22%2C"
            "+%22from%22%3A+100%2C+%22to%22%3A+1000%2C+%22include_lower%22%3A+true"
            "%2C+%22include_upper%22%3A+true%7D"
        )

    def test_not(self):
        actual = SnapshotSearchAPIV2Filter({"q": "test"}).json_filter(
            JsonFilterOperator.not_(self.term_view)
        )
        assert (
            actual._query["jsonFilter"]
            == "%7B%22type%22%3A+%22not%22%2C+%22filter%22%3A+%7B%22type%22%3A"
            "+%22range%22%2C+%22field%22%3A+%22viewCounter%22%2C+%22from%22%3A+100"
            "%2C+%22to%22%3A+1000%2C+%22include_lower%22%3A+true%2C"
            "+%22include_upper%22%3A+true%7D%7D"
        )

    def test_or(self):
        actual = SnapshotSearchAPIV2Filter({"q": "test"}).json_filter(
            JsonFilterOperator.or_(self.term_view, self.term_time)
        )
        assert (
            actual._query["jsonFilter"]
            == "%7B%22type%22%3A+%22or%22%2C+%22filters%22%3A+%5B%7B%22type%22%3A"
            "+%22range%22%2C+%22field%22%3A+%22viewCounter%22%2C+%22from%22%3A+100"
            "%2C+%22to%22%3A+1000%2C+%22include_lower%22%3A+true%2C"
            "+%22include_upper%22%3A+true%7D%2C+%7B%22type%22%3A+%22range%22%2C"
            "+%22field%22%3A+%22startTime%22%2C+%22from%22%3A+%222021-01-01T00%3A00"
            "%3A00%2B09%3A00%22%2C+%22to%22%3A+%222021-12-31T00%3A00%3A00%2B09%3A00"
            "%22%2C+%22include_lower%22%3A+true%2C+%22include_upper%22%3A+true%7D"
            "%5D%7D"
        )

    def test_and(self):
        actual = SnapshotSearchAPIV2Filter({"q": "test"}).json_filter(
            JsonFilterOperator.and_(self.term_view, self.term_time)
        )
        assert (
            actual._query["jsonFilter"]
            == "%7B%22type%22%3A+%22and%22%2C+%22filters%22%3A+%5B%7B%22type%22%3A"
            "+%22range%22%2C+%22field%22%3A+%22viewCounter%22%2C+%22from%22%3A+100"
            "%2C+%22to%22%3A+1000%2C+%22include_lower%22%3A+true%2C"
            "+%22include_upper%22%3A+true%7D%2C+%7B%22type%22%3A+%22range%22%2C"
            "+%22field%22%3A+%22startTime%22%2C+%22from%22%3A+%222021-01-01T00%3A00"
            "%3A00%2B09%3A00%22%2C+%22to%22%3A+%222021-12-31T00%3A00%3A00%2B09%3A00"
            "%22%2C+%22include_lower%22%3A+true%2C+%22include_upper%22%3A+true%7D"
            "%5D%7D"
        )

    def test_nested(self):
        actual = SnapshotSearchAPIV2Filter({"q": "test"}).json_filter(
            JsonFilterOperator.or_(
                JsonFilterOperator.not_(self.term_view), self.term_time
            )
        )
        assert (
            actual._query["jsonFilter"]
            == "%7B%22type%22%3A+%22or%22%2C+%22filters%22%3A+%5B%7B%22type%22%3A"
            "+%22not%22%2C+%22filter%22%3A+%7B%22type%22%3A+%22range%22%2C+%22field"
            "%22%3A+%22viewCounter%22%2C+%22from%22%3A+100%2C+%22to%22%3A+1000%2C"
            "+%22include_lower%22%3A+true%2C+%22include_upper%22%3A+true%7D%7D%2C"
            "+%7B%22type%22%3A+%22range%22%2C+%22field%22%3A+%22startTime%22%2C"
            "+%22from%22%3A+%222021-01-01T00%3A00%3A00%2B09%3A00%22%2C+%22to%22%3A"
            "+%222021-12-31T00%3A00%3A00%2B09%3A00%22%2C+%22include_lower%22%3A"
            "+true%2C+%22include_upper%22%3A+true%7D%5D%7D"
        )

    def test_keyword_undefined(self):
        with self.assertRaises(KeyError) as error:
            SnapshotSearchAPIV2Filter({}).json_filter(
                JsonFilterOperator.or_(
                    JsonFilterOperator.not_(self.term_view), self.term_time
                )
            )
        self.assertEqual(error.exception.args[0], "キーワードが指定されていません")

    def test_no_keyword(self):
        with self.assertRaises(ValueError) as error:
            SnapshotSearchAPIV2Filter({"q": ""}).json_filter(
                JsonFilterOperator.or_(
                    JsonFilterOperator.not_(self.term_view), self.term_time
                )
            )
        self.assertEqual(error.exception.args[0], "JSONフィルタでキーワードなし検索を行うことはできません")


if __name__ == "__main__":
    unittest.main()
