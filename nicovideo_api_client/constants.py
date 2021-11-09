from enum import Enum
from typing import List, Dict, Union, Literal, TypeAlias
from datetime import datetime


class FieldType(Enum):
    CONTENT_ID = "contentId"
    TITLE = "title"
    DESCRIPTION = "description"
    USER_ID = "userId"
    CHANNEL_ID = "channelId"
    VIEW_COUNTER = "viewCounter"
    MYLIST_COUNTER = "mylistCounter"
    LIKE_COUNTER = "likeCounter"
    LENGTH_SECONDS = "lengthSeconds"
    THUMBNAIL_URL = "thumbnailUrl"
    START_TIME = "startTime"
    LAST_RES_BODY = "lastResBody"
    COMMENT_COUNTER = "commentCounter"
    LAST_COMMENT_TIME = "lastCommentTime"
    CATEGORY_TAGS = "categoryTags"
    TAGS = "tags"
    TAGS_EXACT = "tagsExact"
    GENRE = "genre"
    GENRE_KEYWORD = "genre.keyword"


DEFAULT_RETRY = 3

END_POINT_URL_V2 = (
    "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
)
END_POINT_URL_NVV3 = "https://nvapi.nicovideo.jp/v3/"
END_POINT_URL_NVV2 = "https://nvapi.nicovideo.jp/v2/"
END_POINT_URL_VIDEO = "https://www.nicovideo.jp/watch/"
END_POINT_URL_V2_VERSION = "https://api.search.nicovideo.jp/api/v2/snapshot/version"

sort_types = [
    FieldType.VIEW_COUNTER,
    FieldType.MYLIST_COUNTER,
    FieldType.LENGTH_SECONDS,
    FieldType.START_TIME,
    FieldType.COMMENT_COUNTER,
    FieldType.LAST_COMMENT_TIME,
]

target_types = [
    FieldType.CONTENT_ID,
    FieldType.TITLE,
    FieldType.DESCRIPTION,
    FieldType.TAGS,
    FieldType.LAST_RES_BODY,
    FieldType.CATEGORY_TAGS,
    FieldType.TAGS,
    FieldType.TAGS_EXACT,
    FieldType.GENRE,
    FieldType.GENRE_KEYWORD,
]


class SortKeyType(Enum):
    REGISTERED_AT = "registeredAt"


MatchValue: TypeAlias = Union[List[str], List[int], List[datetime]]
RangeLiteral: TypeAlias = Literal["gt", "gte", "lt", "lte"]
RangeValue: TypeAlias = Union[
    Dict[RangeLiteral, str], Dict[RangeLiteral, int], Dict[RangeLiteral, datetime]
]
MatchDict: TypeAlias = Dict[FieldType, MatchValue]
RangeDict: TypeAlias = Dict[FieldType, RangeValue]
CombinedDict: TypeAlias = Dict[FieldType, Union[MatchValue, RangeValue]]
JSON_LITERAL: TypeAlias = str | int | float | bool | None
JSON: TypeAlias = JSON_LITERAL | Dict[str, "JSON"] | List["JSON"]
