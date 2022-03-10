from collections.abc import Set
from datetime import datetime

import requests

from nicovideo_api_client.api.v2.field import SnapshotSearchAPIV2Fields
from nicovideo_api_client.api.v2.targets import SnapshotSearchAPIV2Targets
from nicovideo_api_client.constants import END_POINT_URL_V2_VERSION, FieldType, target_types


class SnapshotSearchAPIV2:
    """
    `ニコニコ動画 『スナップショット検索API v2』 <https://site.nicovideo.jp/search-api-docs/snapshot>`_
    のエンドポイント

    ここの関数から返るオブジェクトをメソッドチェーンをつないで呼び出すことで適切に設定された状態でAPIを叩くことができる。
    """

    @staticmethod
    def tags_exact() -> SnapshotSearchAPIV2Targets:
        """
        タグ検索を行う

        :return: クエリ(キーワード)入力オブジェクト
        """
        return SnapshotSearchAPIV2Targets(FieldType.TAGS_EXACT)

    @staticmethod
    def keywords() -> SnapshotSearchAPIV2Targets:
        """
        キーワード検索を行う

        :return: クエリ(キーワード)入力オブジェクト
        """
        return SnapshotSearchAPIV2Targets(FieldType.TITLE, FieldType.DESCRIPTION, FieldType.TAGS)

    @staticmethod
    def sing_voice_synthesis_tags() -> SnapshotSearchAPIV2Fields:
        """
        VOCALOID・UTAUなどの歌声合成ソフトを利用した動画を検索するタグを用いて検索する。
        タグの一覧は https://lit.link/avogado6 を参照。
        :return: レスポンスフィールドのタイプ指定オブジェクト
        """
        sing_voice_synthesis_tag = [
            "UTAU",
            "VOCALOID",
            "UTAUオリジナル曲",
            "VOCALOIDオリジナル曲",
            "VOICEROIDオリジナル曲",
            "NEUTRINOオリジナル曲",
            "CeVIOオリジナル曲",
            "vocaloid新曲リンク",
            "SynthesizerV",
            "歌うa.i.voice",
            "A.I.VOICEオリジナル曲",
            "歌うボイスロイド",
            "VOCALOIDインスト曲",
            "ボカロオリジナル曲",
            "ソフトウェアシンガー",
            "UTAU新曲リンク",
            "cevio新曲リンク",
            "VOCALOID処女作",
            "UTAU処女作",
            "CeVIO処女作",
            "neutrino(歌声合成エンジン)",
        ]
        exclude = ["ボカロオリジナルを歌ってみた"]
        return SnapshotSearchAPIV2Targets(FieldType.TAGS_EXACT).query(sing_voice_synthesis_tag, exclude)

    @staticmethod
    def targets(targets: Set[FieldType]) -> SnapshotSearchAPIV2Targets:
        """
        検索対象のフィールドタイプを指定して検索を行う。

        :return: クエリ(キーワード)入力オブジェクト
        """

        for t in targets:
            if t not in target_types:
                raise Exception("ターゲットに指定できないフィールドタイプです")

        if FieldType.TAGS_EXACT in targets and len(targets) > 1:
            raise Exception("tagsExact は他のフィールドタイプと併用して指定できません")
        return SnapshotSearchAPIV2Targets(*targets)

    @staticmethod
    def version(timeout: float = 400) -> datetime:
        """
        API の最終更新日時を取得する。

        `データの更新について <https://site.nicovideo.jp/search-api-docs/snapshot#
        %E3%83%87%E3%83%BC%E3%82%BF%E3%81%AE%E6%9B%B4%E6%96%B0%E3%81%AB%E3%81%A
        4%E3%81%84%E3%81%A6>`_ を参照。

        Note: 実際にリクエストが行われる。

        :param timeout: リクエストのタイムアウト時間。
        :return: 最終更新日時
        """
        json = requests.get(END_POINT_URL_V2_VERSION, timeout=timeout).json()
        return datetime.fromisoformat(json["last_modified"])
