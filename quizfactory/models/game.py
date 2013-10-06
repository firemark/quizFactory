from quizfactory import conf
from hashlib import sha1
from random import shuffle, random

__all__ = ["GameQuestion", "Game"]


class GameQuestion(object):
    answers = None
    question = None
    choice = None

    def __init__(self, q):
        self.question = q
        self.answers = { #hash: answer
            sha1(str(random()) + a.text).hexdigest()[:8]: a
            for a in q.answers
        }

        self.choice = self.question.answers_type.set_choice()

    def get_errors(self):
        """Return list of errors (only keys)"""
        return self.question.answers_type.get_errors(self.choice, self.answers)


class Game(object):

    quiz = None
    questions = None
    finish = False

    _pointer = 0

    DIRECTIONS = {"prev": -1, "next": 1}

    def __init__(self, key):
        self.quiz = conf.quizzes[key]

        self.questions = [GameQuestion(q) for q in self.quiz.questions]
        shuffle(self.questions)

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
