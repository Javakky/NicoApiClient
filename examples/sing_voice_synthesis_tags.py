from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2
from nicovideo_api_client.constants import FieldType


def main():
    # URL生成
    request = (
        SnapshotSearchAPIV2()
        .sing_voice_synthesis_tags()
        .field({FieldType.TITLE})
        .sort(FieldType.VIEW_COUNTER)
        .no_filter()
        .limit(10)
        .user_agent("NicoApiClient", "0.5.0")
    )

    print(request.request().json())


if __name__ == "__main__":
    main()
