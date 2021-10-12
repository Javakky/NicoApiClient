import sys

sys.path.append(".")

from examples import json_filter, version, simple, multiple

if __name__ == "__main__":
    simple.main()
    json_filter.main()
    multiple.main()
    version.main()
