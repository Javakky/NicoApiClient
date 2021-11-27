import sys

sys.path.append(".")

from examples import json_filter, multiple, simple, simple_filter, version

if __name__ == "__main__":
    simple.main()
    simple_filter.main()
    json_filter.main()
    multiple.main()
    version.main()
