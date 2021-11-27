from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import (
    CombinedDict,
    FieldType,
    MatchDict,
    MatchValue,
    RangeDict,
    RangeValue,
)


def main():
    """一致検索の場合"""
    # フィルタの指定
    view: MatchValue = [100, 1000, 10000]
    mylist: MatchValue = [10, 100]
    match_filter: MatchDict = {
        FieldType.VIEW_COUNTER: view,
        FieldType.MYLIST_COUNTER: mylist,
    }

    # URL生成
    request = (
        SnapshotSearchAPIV2()
        .tags_exact()
        .query("VOCALOID")
        .field(
            {
                FieldType.TITLE,
                FieldType.DESCRIPTION,
                FieldType.VIEW_COUNTER,
                FieldType.MYLIST_COUNTER,
            }
        )
        .sort(FieldType.VIEW_COUNTER)
        .simple_filter()
        .filter(match_filter)
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
        .field(
            {
                FieldType.TITLE,
                FieldType.DESCRIPTION,
                FieldType.VIEW_COUNTER,
                FieldType.MYLIST_COUNTER,
            }
        )
        .sort(FieldType.VIEW_COUNTER)
        .simple_filter()
        .filter(range_filter)
        .limit(100)
    )

    print(request.build_url())

    # 実行
    # API のレスポンスが表示される
    print(request.request().json())

    """複合検索の場合"""
    # フィルタの指定
    view: MatchValue = [1000, 10000]
    mylist: RangeValue = {"gt": 10, "lte": 100}
    combined_filter: CombinedDict = {
        FieldType.VIEW_COUNTER: view,
        FieldType.MYLIST_COUNTER: mylist,
    }
    combine: bool = True

    # URL生成
    request = (
        SnapshotSearchAPIV2()
        .tags_exact()
        .query("VOCALOID")
        .field(
            {
                FieldType.TITLE,
                FieldType.DESCRIPTION,
                FieldType.VIEW_COUNTER,
                FieldType.MYLIST_COUNTER,
            }
        )
        .sort(FieldType.VIEW_COUNTER)
        .simple_filter()
        .filter(combined_filter, combine)
        .limit(100)
    )

    print(request.build_url())

    # 実行
    # API のレスポンスが表示される
    print(request.request().json())


if __name__ == "__main__":
    main()
