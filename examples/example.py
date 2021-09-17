import datetime

import sys

from nicovideo_api_client.api.v2.json_filter import JsonFilterOperator, JsonFilterTerm

sys.path.append(".")

from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import FieldType

# URL生成
request = SnapshotSearchAPIV2() \
    .tags_exact() \
    .query("VOCALOID") \
    .field({FieldType.TITLE, FieldType.CONTENT_ID}) \
    .sort(FieldType.VIEW_COUNTER) \
    .simple_filter().filter() \
    .limit(100)

# https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search?targets=tagsExact&q=VOCALOID&fields=contentId%2Ctitle&_sort=-viewCounter
print(request.build_url())

# 実行
# API のレスポンスが表示される
print(request.request().json())

# jsonFilter を利用したリクエスト
request = SnapshotSearchAPIV2() \
    .tags_exact() \
    .query("VOCALOID") \
    .field({FieldType.TITLE}) \
    .sort(FieldType.VIEW_COUNTER) \
    .json_filter(
        JsonFilterOperator.not_(
            JsonFilterTerm.set_range_time(
                end=datetime.datetime(2021, 1, 1, 0, 0, 0),
                include_upper=False
            )
        )
    ).limit(10)

print(request.build_url())
print(request.request().json())
