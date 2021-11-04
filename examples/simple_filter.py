from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import (
    FieldType,
    MatchDict,
    RangeDict,
    MatchValue,
    RangeValue,
)


def main():
    """一致検索の場合"""
    # フィルタの指定
    title: MatchValue = ["初音ミク", "鏡音リン", "GUMI"]
    description: MatchValue = ["初投稿", "1作目"]
    match_filter: MatchDict = {
        FieldType.TITLE: title,
        FieldType.DESCRIPTION: description,
    }

    # URL生成
    request = (
        SnapshotSearchAPIV2()
        .tags_exact()
        .query("VOCALOID")
        .field({FieldType.TITLE, FieldType.DESCRIPTION})
        .sort(FieldType.VIEW_COUNTER)
        .simple_filter(match_filter)
        .filter()
        .limit(100)
    )

    print(request.build_url())

    # 実行
    # API のレスポンスが表示される
    print(request.request().json())

    """範囲検索の場合"""
    # フィルタの指定
    view: RangeValue = {"gte": 1000, "lt": 10000}
    mylist: RangeValue = {"gt": 10, "lte": 100}
    range_filter: RangeDict = {
        FieldType.VIEW_COUNTER: view,
        FieldType.MYLIST_COUNTER: mylist,
    }

    # URL生成
    request = (
        SnapshotSearchAPIV2()
        .tags_exact()
        .query("VOCALOID")
        .field({FieldType.TITLE, FieldType.DESCRIPTION})
        .sort(FieldType.VIEW_COUNTER)
        .simple_filter(range_filter)
        .filter()
        .limit(100)
    )

    print(request.build_url())

    # 実行
    # API のレスポンスが表示される
    print(request.request().json())


if __name__ == "__main__":
    main()
