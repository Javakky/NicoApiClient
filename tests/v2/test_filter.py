import unittest

from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import FieldType


class SnapshotSearchAPIV2FieldsTestCase(unittest.TestCase):
    def test_no_keyword_no_filter(self):
        with self.assertRaises(ValueError):
            SnapshotSearchAPIV2().keywords().no_keyword().field({FieldType.TITLE}).sort(
                FieldType.VIEW_COUNTER
            ).no_filter()
