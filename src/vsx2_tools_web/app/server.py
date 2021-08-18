import sys
import argparse

from waitress import serve

from . import app

import logging

log = logging.getLogger(__name__)


def main(argv=sys.argv):
    description = """
        Start server.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("secret_key", metavar="secret")
    parser.add_argument("-s", "--host", dest="host", help="Host", default="0.0.0.0")

    parser.add_argument(
        "-p", "--port", dest="port", default=8080, type=int, help="Port"
    )

    args = parser.parse_args(argv[1:])
    app.config["SECRET_KEY"] = args.secret_key

    serve(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
