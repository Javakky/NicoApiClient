import unittest

from nicovideo_api_client.api.v2.field import SnapshotSearchAPIV2Fields
from nicovideo_api_client.constants import FieldType


class SnapshotSearchAPIV2FieldsTestCase(unittest.TestCase):
    @staticmethod
    def test_field_noting():
        assert "fields" not in SnapshotSearchAPIV2Fields({}).field(set())._query

    @staticmethod
    def test_field_once():
        assert (
            SnapshotSearchAPIV2Fields({}).field({FieldType.TITLE})._query["fields"]
            == "title"
        )

    @staticmethod
    def test_field_multi():
        assert (
            SnapshotSearchAPIV2Fields({})
            .field({FieldType.TITLE, FieldType.DESCRIPTION})
            ._query["fields"]
            == "description,title"
        )


if __name__ == "__main__":
    unittest.main()
