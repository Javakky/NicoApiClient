import sys

sys.path.append(".")

from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import FieldType

# URL生成
url = SnapshotSearchAPIV2() \
    .tags_exact() \
    .q("VOCALOID") \
    .field({FieldType.TITLE, FieldType.CONTENT_ID}) \
    .sort(FieldType.VIEW_COUNTER) \
    .simple_filter().filter() \
    .limit(100) \
    .build_url()

# https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search?targets=tagsExact&q=VOCALOID&fields=contentId%2Ctitle&_sort=-viewCounter
print(url)

# 実行
json = SnapshotSearchAPIV2() \
    .tags_exact() \
    .q("VOCALOID") \
    .field({FieldType.TITLE, FieldType.CONTENT_ID}) \
    .sort(FieldType.VIEW_COUNTER) \
    .simple_filter().filter() \
    .limit(100) \
    .request() \
    .json()

# API のレスポンスが表示される
print(json)
