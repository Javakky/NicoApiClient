from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import FieldType


def main():
    # URL生成
    request = (
        SnapshotSearchAPIV2()
        .tags_exact()
        .query("VOCALOID")
        .field({FieldType.TITLE, FieldType.DESCRIPTION})
        .sort(FieldType.VIEW_COUNTER)
        .no_filter()
        .limit(100)
        .user_agent("NicoApiClient", "0.5.0")
    )

    # https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search?targets=tagsExact&q=VOCALOID&fields=contentId%2Ctitle&_sort=-viewCounter
    print(request.build_url())

    # 実行
    # API のレスポンスが表示される
    print(request.request().json())


if __name__ == "__main__":
    main()
