# NicoApiClient

## 概要
[ニコニコ動画 『スナップショット検索API v2』](https://site.nicovideo.jp/search-api-docs/snapshot) などの API について、仕様をなるべく意識せずに利用できるクライアントを提供する。

## example
```python
from nicovideo_api_client.nicovideo.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.nicovideo.constants import FieldType

json = SnapshotSearchAPIV2() \
    .tagsExact() \
    .q("VOCALOID") \
    .field({FieldType.TITLE, FieldType.CONTENT_ID}) \
    .sort(FieldType.VIEW_COUNTER) \
    .simple_filter().filter() \
    .limit(100) \
    .request() \
    .json()
```