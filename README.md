# NicoApiClient

## 概要
[ニコニコ動画 『スナップショット検索API v2』](https://site.nicovideo.jp/search-api-docs/snapshot) などの API について、仕様をなるべく意識せずに利用できるクライアントを提供する。

## install

```shell
pip install nicovideo-api-client
```

## example

```python
from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import FieldType

json = SnapshotSearchAPIV2() \
    .tags_exact() \
    .query("VOCALOID") \
    .field({FieldType.TITLE, FieldType.CONTENT_ID}) \
    .sort(FieldType.VIEW_COUNTER) \
    .simple_filter().filter() \
    .limit(100) \
    .request() \
    .json()
```

## 利用規約

https://site.nicovideo.jp/search-api-docs/snapshot#api%E5%88%A9%E7%94%A8%E8%A6%8F%E7%B4%84
