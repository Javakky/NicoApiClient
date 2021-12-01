from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import FieldType


def main():
    """キーワード指定について"""
    # URL生成
    # AND・OR検索を使う場合には、query()およびand_()を呼び出し、「文字列」または「検索ワードを文字列要素として持つリスト」を指定する。
    # 1つのキーワードのみを指定する場合には、single_queryを呼び出し「文字列」を指定する。
    request = (
        SnapshotSearchAPIV2()
        .tags_exact()
        .query("VOCALOID")
        .and_(["初音ミク", "鏡音リン"])
        .and_(["MMD"])
        .field({FieldType.TITLE})
        .sort(FieldType.VIEW_COUNTER)
        .simple_filter()
        .filter()
        .limit(100)
        .user_agent("NicoApiClient", "0.5.0")
    )

    print(request.build_url())

    # 実行
    # API のレスポンスが表示される
    print(request.request().json())


if __name__ == "__main__":
    main()
