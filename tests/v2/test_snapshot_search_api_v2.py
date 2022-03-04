import unittest

import pytest as pytest

from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import FieldType, target_types


class SnapshotSearchAPIV2TestCase(unittest.TestCase):
    @staticmethod
    def test_tags_exact():
        instance = SnapshotSearchAPIV2().tags_exact()
        assert instance._query == {"targets": "tagsExact"}

    @staticmethod
    def test_keywords():
        instance = SnapshotSearchAPIV2().keywords()
        assert instance._query == {"targets": "title,description,tags"}

    @staticmethod
    def test_sing_voice_synthesis_tags():
        instance = SnapshotSearchAPIV2().sing_voice_synthesis_tags().field(set())
        assert instance._query == {
            "targets": "tagsExact",
            "q": "UTAU OR VOCALOID OR UTAUオリジナル曲 OR VOCALOIDオリジナル曲 OR VOICEROIDオリジナル曲 OR NEUTRINOオリジナル曲 OR "
            "CeVIOオリジナル曲 OR vocaloid新曲リンク OR SynthesizerV OR 歌うa.i.voice OR A.I.VOICEオリジナル曲 OR 歌うボイスロイド OR "
            "VOCALOIDインスト曲 OR ボカロオリジナル曲 OR ソフトウェアシンガー OR UTAU新曲リンク OR cevio新曲リンク OR VOCALOID処女作 OR UTAU処女作 OR "
            "CeVIO処女作 OR neutrino(歌声合成エンジン) -ボカロオリジナルを歌ってみた",
        }

    def test_targets_success(self):
        for t in target_types:
            with self.subTest(t.value):
                instance = SnapshotSearchAPIV2().targets({t})
                assert instance._query == {"targets": t.value}

    @staticmethod
    def test_targets_fail_multiple_tags_exact():
        with pytest.raises(Exception) as e:
            SnapshotSearchAPIV2().targets({FieldType.TITLE, FieldType.TAGS_EXACT})
        assert "tagsExact は他のフィールドタイプと併用して指定できません" == str(e.value)

    def test_targets_fail_not_available(self):
        for t in set(FieldType).difference(set(target_types)):
            with self.subTest(t.value):
                with pytest.raises(Exception) as e:
                    SnapshotSearchAPIV2().targets({t})
                assert "ターゲットに指定できないフィールドタイプです" == str(e.value)


if __name__ == "__main__":
    unittest.main()
