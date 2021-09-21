import unittest

from nicovideo_api_client.api.v2.field import SnapshotSearchAPIV2Fields
from nicovideo_api_client.constants import FieldType


class SnapshotSearchAPIV2FieldsTestCase(unittest.TestCase):
    def test_field_noting(self):
        assert "fields" not in SnapshotSearchAPIV2Fields({}).field(set())._query

    def test_field_once(self):
        assert SnapshotSearchAPIV2Fields({}).field({FieldType.TITLE})._query["fields"] == "title"

    def test_field_multi(self):
        assert SnapshotSearchAPIV2Fields({}).field({FieldType.TITLE, FieldType.DESCRIPTION})._query["fields"] \
               == "description,title"


if __name__ == '__main__':
    unittest.main()
