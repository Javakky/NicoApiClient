import unittest
from datetime import datetime

from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import FieldType


class SnapshotSearchAPIV2UserAgentTestCase(unittest.TestCase):
    def undefined_user_agent_product(self):
        with self.assertRaises(ValueError) as error:
            SnapshotSearchAPIV2().targets({FieldType.TITLE}).query("テスト").field(
                {FieldType.TITLE}
            ).sort(FieldType.VIEW_COUNTER).simple_filter().filter().limit(
                10
            ).user_agent(
                version="0.5.0"
            )
        self.assertEqual(error.exception.args[0], "User-Agentのプロダクト名の指定は必須です")

    def undefined_user_agent_version(self):
        with self.assertRaises(ValueError) as error:
            SnapshotSearchAPIV2().targets({FieldType.TITLE}).query("テスト").field(
                {FieldType.TITLE}
            ).sort(FieldType.VIEW_COUNTER).simple_filter().filter().limit(
                10
            ).user_agent(
                product="NicoApiClient"
            )
        self.assertEqual(error.exception.args[0], "User-Agentのプロダクトバージョンの指定は必須です")


if __name__ == "__main__":
    unittest.main()
