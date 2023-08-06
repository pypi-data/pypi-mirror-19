import argparse
import email
import inspect
import logging
import sys

import pkg_resources

log = logging.getLogger(__name__)


def setup():
    parser = argparse.ArgumentParser()
    parser.add_argument("--desc", "-D", action="store_true", help="desc")
    parser.add_argument("--version", "-V", action="store_true", help="version")

    subparsers = parser.add_subparsers(help="sub-command help")

    for module_name in ["example", "list", "process", "profile", "server", "shell", "start"]:
        module = inspect.importlib.import_module("{}.{}".format(
            sys.modules[__name__].__package__, module_name
        ))
        module_parser = subparsers.add_parser(module_name, description=module.__doc__)
        module.setup(module_parser)
        module_parser.set_defaults(main=module.main)
    return parser


def main():
    try:
        parser = setup()
        options = parser.parse_args()
        pkg = pkg_resources.get_distribution(__name__.split(".")[0])
        pkg_info = email.message_from_string(pkg.get_metadata("PKG-INFO"))

        if options.desc:
            print(pkg_info.get("Summary"))
        elif options.version:
            print(pkg.version)
        else:
            options.main(options)
    except Exception as e:
        log.exception(e)
