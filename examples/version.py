from nicovideo_api_client.api.v2.snapshot_search_api_v2 import SnapshotSearchAPIV2


def main():
    print("latest update date: " + SnapshotSearchAPIV2().version().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    main()
