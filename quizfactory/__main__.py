from quizfactory import app, conf
from os import path
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

    return parser


def run(args):

    conf.load_conf(args)

    app.debug = True
    app.template_folder = path.join(BASEDIR, "templates")
    app.static_folder = path.join(BASEDIR, "static")
    app.config['SECRET_KEY'] = "Koszmar firemarka"
    app.run(args.host, args.port)

if __name__ == '__main__':
    parser = set_parser()
    args = parser.parse_args()
    run(args)
