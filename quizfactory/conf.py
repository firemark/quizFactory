settings = None
urls = {
    "index": "/",
    "quiz": "/quiz/<int:quiz_id>/",
    "question": "/quiz/<int:quiz_id>/question/<direction>/",
}
quizzes = []


def load_conf():
    global settings
    # todo
    settings = __import__("settings")
