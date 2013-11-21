from quizfactory import app, conf
from os import path, mkdir, chmod
from session import SqliteSessionInterface
import argparse

BASEDIR = path.dirname(__file__)


def set_parser():
    parser = argparse.ArgumentParser(description='run site with quizzes')
    parser.add_argument('-q', '--qpath', metavar='QUIZZES_PATH', type=str,
                        default=path.join(BASEDIR, "quizzes"),
                        help='path to quizzes dir')
    parser.add_argument('-f', '--format', metavar='FORMAT', default='xml',
                        help='format of file [now only xml]')
    parser.add_argument('-p', '--port', metavar='PORT', default=8000,
                        type=int, help='Port of server')
    parser.add_argument('-H', '--host', metavar='HOST', default='0.0.0.0',
                        type=str, help='Host of server')
    parser.add_argument('-d', '--debug', default=False, action='store_const',
                        const=True, help='run in debug mode')

    return parser


def setup(args):

    conf.load_conf(args)

    app.debug = args.debug
    app.template_folder = path.join(BASEDIR, "templates")
    app.static_folder = path.join(BASEDIR, "static")
    session_dir = getattr(args, "session_dir", "/tmp/quizfactory/")

    if not path.exists(session_dir):
        mkdir(session_dir)
        chmod(session_dir, int('700', 8))

    app.config['SECRET_KEY'] = getattr(args, 'SECRET_KEY', "Koszmar firemarka")
    app.session_interface = SqliteSessionInterface(session_dir)

if __name__ == '__main__':
    parser = set_parser()
    args = parser.parse_args()
    setup(args)
    app.run(args.host, args.port)
