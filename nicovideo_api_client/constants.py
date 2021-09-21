from enum import Enum


class FieldType(Enum):
    CONTENT_ID = 'contentId'
    TITLE = 'title'
    DESCRIPTION = 'description'
    VIEW_COUNTER = 'viewCounter'
    MYLIST_COUNTER = 'mylistCounter'
    LENGTH_SECONDS = 'lengthSeconds'
    THUMBNAIL_URL = 'thumbnailUrl'
    START_TIME = 'startTime'
    LAST_RES_BODY = 'lastResBody'
    COMMENT_COUNTER = 'commentCounter'
    LAST_COMMENT_TIME = 'lastCommentTime'
    CATEGORY_TAGS = 'categoryTags'
    TAGS = 'tags'
    TAGS_EXACT = 'tagsExact'
    GENRE = 'genre'
    GENRE_KEYWORD = 'genre.keyword'


END_POINT_URL_V2 = 'https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search'
END_POINT_URL_NVV3 = 'https://nvapi.nicovideo.jp/v3/'
END_POINT_URL_NVV2 = 'https://nvapi.nicovideo.jp/v2/'
END_POINT_URL_VIDEO = 'https://www.nicovideo.jp/watch/'
END_POINT_URL_V2_VERSION = 'https://api.search.nicovideo.jp/api/v2/snapshot/version'

sort_types = [
    FieldType.VIEW_COUNTER,
    FieldType.MYLIST_COUNTER,
    FieldType.LENGTH_SECONDS,
    FieldType.START_TIME,
    FieldType.COMMENT_COUNTER,
    FieldType.LAST_COMMENT_TIME
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
    FieldType.GENRE_KEYWORD
]


class SortKeyType(Enum):
    REGISTERED_AT = 'registeredAt'
