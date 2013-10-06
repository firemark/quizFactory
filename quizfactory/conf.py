from quizfactory.models import Quiz

from os import path, listdir
from hashlib import sha1


settings = None
urls = {
    "index": "/",
    "quiz": "/quiz/<quiz_id>/",
    "question": "/quiz/<quiz_id>/question/<direction>/",
}
quizzes = {}  # hash: Quiz(...)


def load_conf(args):
    global quizzes
    # todo
    #settings = __import__("settings")

    print("Loading quizzes...")
    qpath = args.qpath
    files = listdir(qpath)

    for filename in files:
        quiz = Quiz.load_from_file(path.join(qpath, filename))

        print("---", filename)
        m = sha1()
        m.update(filename.encode('utf-8'))
        m.update(qpath.encode('utf-8'))
        key = m.hexdigest()[:8]

        quiz.key = key
        quizzes[key] = quiz

    print("Loading views...")
    for name in urls.keys():
        __import__("views.%s" % name)
    print("Done.")
