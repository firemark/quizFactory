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

    return parser


def run(args):

    conf.load_conf(args)

    app.debug = True
    app.template_folder = path.join(BASEDIR, "templates")
    app.static_folder = path.join(BASEDIR, "static")
    app.run()

if __name__ == '__main__':
    parser = set_parser()
    args = parser.parse_args()
    run(args)
