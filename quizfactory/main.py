from quizfactory import app, conf
from quizfactory.models import Quiz

from os import path, listdir
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

    print("Loading quizzes...")
    qpath = args.qpath
    files = listdir(qpath)

    conf.quizzes = [Quiz.load_from_file(path.join(qpath, filename))
                    for filename in files]

    print("Loading views...")
    for name in conf.urls.keys():
        __import__("views.%s" % name)
    print("Done.")

    app.debug = True
    app.run()

if __name__ == '__main__':
    parser = set_parser()
    args = parser.parse_args()
    run(args)
