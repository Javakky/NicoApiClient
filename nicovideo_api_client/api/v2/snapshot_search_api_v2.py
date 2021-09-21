from collections.abc import Set
from datetime import datetime

import requests

from nicovideo_api_client.api.v2.targets import SnapshotSearchAPIV2Targets
from nicovideo_api_client.constants import END_POINT_URL_V2_VERSION, FieldType, target_types


class SnapshotSearchAPIV2:
    """
    `ニコニコ動画 『スナップショット検索API v2』 <https://site.nicovideo.jp/search-api-docs/snapshot>`_ のエンドポイント
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
