
import sys

sys.path.append("/runner-venv/lib/python3.11/site-packages")

# Some libs (e.g.: Jinja2) get confused if the app is not launched from the directory where
# main.py is so here we create a launcher to call the app_executor instead of using it via
# the runtime_tools directly.

import runtime_tools.app_executor as app_executor


def main():
    app_executor.main()


if __name__ == "__main__":  # pragma: no cover
    main()

