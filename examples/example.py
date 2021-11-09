import sys

sys.path.append(".")

from examples import json_filter, version, simple, simple_filter, multiple

if __name__ == "__main__":
    simple.main()
    simple_filter.main()
    json_filter.main()
    multiple.main()
    version.main()
