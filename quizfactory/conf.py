settings = None
urls = {
    "index": "/",
    "quiz": "/quiz/<quiz>/",
    "question": "/quiz/<quiz>/question/<direction>/",
}


def load_conf():
    global settings
    #todo
    settings = __import__("settings")