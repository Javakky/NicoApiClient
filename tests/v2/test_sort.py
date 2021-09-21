import unittest

import pytest

from nicovideo_api_client.api.v2.sort import SnapshotSearchAPIV2Sort
from nicovideo_api_client.constants import FieldType, sort_types


class SnapshotSearchAPIV2SortTestCase(unittest.TestCase):
    def test_sort_plus_success(self):
        for t in sort_types:
            with self.subTest(t.value):
                assert SnapshotSearchAPIV2Sort({}).sort(t, True)._query["_sort"] == ("+" + t.value)

    def test_sort_minus_success(self):
        for t in sort_types:
            with self.subTest(t.value):
                assert SnapshotSearchAPIV2Sort({}).sort(t, False)._query["_sort"] == ("-" + t.value)

    def test_sort_fail_not_available(self):
        for t in set(FieldType).difference(set(sort_types)):
            with self.subTest(t.value):
                with pytest.raises(Exception) as e:
                    SnapshotSearchAPIV2Sort({}).sort(t, True)
                assert "不正なソートタイプ" == str(e.value)


if __name__ == '__main__':
    unittest.main()
