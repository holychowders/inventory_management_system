import logging
from pprint import pformat

from db import all_products, ensure_db


def main() -> None:
    ensure_db()
    logging.info("Products:\n%s", pformat(all_products()))


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    main()
