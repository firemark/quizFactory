from quizfactory import conf
from random import shuffle


class Game(object):

    quiz = None
    questions = None

    _pointer = 0

    DIRECTIONS = {"prev": -1, "next": 1}

    def __init__(self, key):
        self.quiz = conf.quizzes[key]

        self.questions = self.quiz.questions[:]
        shuffle(self.questions)

    @property
    def now_question(self):
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
            return change_pointer(pointer)

    @property
    def is_last(self):
        return self._pointer < len(self.questions)

    @property
    def is_first(self):
        return self._pointer >= 0

    @property
    def pointer(self):
        return self._pointer
    
