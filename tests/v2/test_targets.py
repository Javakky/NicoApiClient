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
    def test_single_query():
        expected = "keyword"
        assert SnapshotSearchAPIV2Targets(FieldType.TITLE).single_query(expected)._query["q"] == expected

    @staticmethod
    def test_query():
        expected = "keyword"
        assert SnapshotSearchAPIV2Targets(FieldType.TITLE).query([expected])._query["q"] == expected

    @staticmethod
    def test_query_escape_space():
        expected = '"1 2"'
        assert SnapshotSearchAPIV2Targets(FieldType.TITLE).query(["1 2"])._query["q"] == expected

    @staticmethod
    def test_query_escape_or():
        expected = '"OR"'
        assert SnapshotSearchAPIV2Targets(FieldType.TITLE).query(["OR"])._query["q"] == expected

    @staticmethod
    def test_query_escape_double_quote():
        expected = '"\\"keyword\\""'
        assert SnapshotSearchAPIV2Targets(FieldType.TITLE).query(['"keyword"'])._query["q"] == expected

    @staticmethod
    def test_query_escape_double_backslash():
        expected = '"keyword\\\\"'
        assert SnapshotSearchAPIV2Targets(FieldType.TITLE).query(["keyword\\"])._query["q"] == expected

    @staticmethod
    def test_query_and():
        expected = "VOCALOID UTAU"
        assert SnapshotSearchAPIV2Targets(FieldType.TITLE).query(["VOCALOID"]).and_("UTAU")._query["q"] == expected

    @staticmethod
    def test_query_and_or():
        expected = "VOCALOID OR UTAU SynthesizerV"
        assert (
            SnapshotSearchAPIV2Targets(FieldType.TITLE).query(["VOCALOID", "UTAU"]).and_("SynthesizerV")._query["q"]
            == expected
        )

    @staticmethod
    def test_query_and_or_not():
        expected = "VOCALOID OR UTAU SynthesizerV -CeVIO"
        assert (
            SnapshotSearchAPIV2Targets(FieldType.TITLE)
            .query(["VOCALOID", "UTAU"], ["CeVIO"])
            .and_("SynthesizerV")
            .field(set())
            ._query["q"]
            == expected
        )

    @staticmethod
    def test_query_or_not():
        expected = "VOCALOID OR UTAU -CeVIO"
        assert (
            SnapshotSearchAPIV2Targets(FieldType.TITLE).query(["VOCALOID", "UTAU"], ["CeVIO"]).field(set())._query["q"]
            == expected
        )


if __name__ == "__main__":
    unittest.main()
