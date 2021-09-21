import unittest

from nicovideo_api_client.api.v2.limit import SnapshotSearchAPIV2Limit


class SnapshotSearchAPIV2LimitTestCase(unittest.TestCase):
    def test_limit_default(self):
        assert SnapshotSearchAPIV2Limit({}).limit()._limit == 10

    def test_limit(self):
        assert SnapshotSearchAPIV2Limit({}).limit(100)._limit == 100


if __name__ == '__main__':
    unittest.main()
