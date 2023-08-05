import argparse

parser = argparse.ArgumentParser(description="Python Version Of Flyway. Dependencies: sqlalchemy, oursql")
parser.add_argument('cmd', nargs='+', help="command")
parser.add_argument('--url', help="database url")
parser.add_argument('--location', help="script files location")
parser.add_argument('--pattern', help="script file pattern")
parser.add_argument('--debug', action="store_true", help="whether to turn on debug log")
# parser.add_argument('--list-installed', action="store_true", help="list installed scripts")
# parser.add_argument('--list-uninstalled', action="store_true", help="list uninstalled scripts")
# parser.add_argument('--install', help="script version to install")
#
parser.add_argument('--config', help="config file location")
# parser.add_argument('--list-config', action="store_true", help="only list config")
# parser.add_argument('--validate', action="store_true", help="only check")
cmd_conf, _ = parser.parse_known_args()
print cmd_conf.__dict__
