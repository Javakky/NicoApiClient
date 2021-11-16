from enum import Enum
from typing import List, Dict, Union, Literal, TypeAlias
from datetime import datetime


class FieldType(Enum):
    """コンテンツのフィールド種別"""

    CONTENT_ID = "contentId"
    """コンテンツID
    https://nico.ms/ の後に連結することでコンテンツへのURLになります
    """

    TITLE = "title"
    """タイトル"""

    DESCRIPTION = "description"
    """コンテンツの説明文"""

    USER_ID = "userId"
    """ユーザー投稿動画の場合、投稿者のユーザーID"""

    CHANNEL_ID = "channelId"
    """	チャンネル動画の場合、チャンネルID"""

    VIEW_COUNTER = "viewCounter"
    """再生数"""

    MYLIST_COUNTER = "mylistCounter"
    """マイリスト数またはお気に入り数"""

    LIKE_COUNTER = "likeCounter"
    """いいね！数"""

    LENGTH_SECONDS = "lengthSeconds"
    """再生時間(秒)"""

    THUMBNAIL_URL = "thumbnailUrl"
    """サムネイルのURL"""

    START_TIME = "startTime"
    """コンテンツの投稿時間"""

    LAST_RES_BODY = "lastResBody"
    """最新のコメント"""

    COMMENT_COUNTER = "commentCounter"
    """コメント数"""

    LAST_COMMENT_TIME = "lastCommentTime"
    """最終コメント時間"""

    CATEGORY_TAGS = "categoryTags"
    """カテゴリタグ"""

    TAGS = "tags"
    """タグ(空白区切り)"""

    TAGS_EXACT = "tagsExact"
    """タグ完全一致(空白区切り)"""

    GENRE = "genre"
    """ジャンル"""

    GENRE_KEYWORD = "genre.keyword"
    """ジャンル完全一致"""


DEFAULT_RETRY = 3

END_POINT_URL_V2 = (
    "https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search"
)
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
