from quizfactory import conf
from hashlib import sha1
from random import shuffle, random


class GameQuestion(object):
    answers = None
    question = None
    choice = None

    def __init__(self, q):
        self.question = q
        self.answers = {
            sha1(str(random()) + a.text).hexdigest()[:8]: a
            for a in q.answers
        }

        t = self.question.answers_type

        if t == "radio":
            self.choice = ""  # nothing selected
        elif t == "checkbox":
            self.choice = []  # list of selected answers
        elif t == "text":
            self.choice = ""  # text

    def get_errors(self):
        """Return list of errors (only key)"""
        t = self.question.answers_type
        choice = self.choice
        items = self.answers.items

        if t == "radio":
            good_answers = [k for k, v in items() if v.is_correct]
            return [self.choice] if choice in good_answers else []
        elif t == "checkbox":
            good_answers = {k for k, v in items() if v.is_correct}
            return list(set(choice) & good_answers)
        elif t == "text":
            return [k for k, v in items() if v.is_correct and v.text == choice]

        return []  # if is OK - send empty list


class Game(object):

    quiz = None
    questions = None
    answers = None
    finish = False

    _pointer = 0

    DIRECTIONS = {"prev": -1, "next": 1}

    def __init__(self, key):
        self.quiz = conf.quizzes[key]

        self.questions = [GameQuestion(q) for q in self.quiz.questions]
        shuffle(self.questions)
        self.answers = [{} for _ in range(len(self.questions))]

    @property
    def get_question(self):
        return self.questions[self._pointer]

    def change_pointer(self, pointer):
        if pointer in range(len(self.questions)):
            self._pointer = pointer
            return True
        else:
            return False

    def move(self, direction):
        try:
            pointer = self._pointer + self.DIRECTIONS[direction]
        except KeyError:
            return False
        else:
            return self.change_pointer(pointer)

    @property
    def is_last(self):
        return self._pointer < len(self.questions)

    @property
    def is_first(self):
        return self._pointer >= 0

    @property
    def pointer(self):
        return self._pointer
