import unittest

import pytest

from nicovideo_api_client.api.v2.targets import SnapshotSearchAPIV2Targets
from nicovideo_api_client.constants import FieldType


class SnapshotSearchAPIV2TargetsTestCase(unittest.TestCase):
    @staticmethod
    def test_init_fail():
        with pytest.raises(Exception) as e:
            SnapshotSearchAPIV2Targets()
        assert "targets が設定されていません" == str(e.value)

    @staticmethod
    def test_query():
        expected = "keyword"
        assert SnapshotSearchAPIV2Targets(FieldType.TITLE).query(expected)._query["q"] == expected


if __name__ == "__main__":
    unittest.main()
