from datetime import datetime

from nicovideo_api_client.api.v2.json_filter import JsonFilterOperator, JsonFilterTerm
from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import FieldType


def main():
    # URL生成
    request = (
        SnapshotSearchAPIV2()
        .tags_exact()
        .query("VOCALOID")
        .and_(["初音ミク", "鏡音リン"])
        .and_(["MMD"])
        .field({FieldType.TITLE})
        .sort(FieldType.VIEW_COUNTER)
        .json_filter(
            JsonFilterOperator.or_(
                JsonFilterTerm.set_range_time(
                    from_=datetime(2021, 1, 1, 0, 0, 0), include_lower=True
                ),
                JsonFilterTerm.set_range_time(to_=datetime(2010, 1, 1, 0, 0, 0)),
            )
        )
        .limit(10)
    )

    # https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search?targets=tagsExact&q=VOCALOID&fields=title&_sort=-viewCounter&jsonFilter=%7B%22type%22%3A+%22or%22%2C+%22filters%22%3A+%5B%7B%22type%22%3A+%22range%22%2C+%22field%22%3A+%22startTime%22%2C+%22from%22%3A+%222021-01-01T00%3A00%3A00%2B09%3A00%22%2C+%22include_lower%22%3A+true%2C+%22include_upper%22%3A+true%7D%2C+%7B%22type%22%3A+%22range%22%2C+%22field%22%3A+%22startTime%22%2C+%22to%22%3A+%222010-01-01T00%3A00%3A00%2B09%3A00%22%2C+%22include_lower%22%3A+true%2C+%22include_upper%22%3A+true%7D%5D%7D
    print(request.build_url())
    print(request.request().json())


if __name__ == "__main__":
    main()
