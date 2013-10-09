from quizfactory import conf
from hashlib import sha1
from random import shuffle, random

__all__ = ["GameQuestion", "Game"]


class GameQuestion(object):
    answers = None
    question = None
    good_answers = []
    choice = None

    def __init__(self, q):
        self.question = q
        random_str = str(random()).encode('utf-8')
        self.answers = {  # hash: answer
            sha1(random_str + a.text.encode('utf-8')).hexdigest()[:8]: a
            for a in q.answers
        }

        self.choice = self.question.answers_type.set_choice()

    def get_errors(self):
        """Return list of errors (only keys)"""
        return self.question.answers_type.get_errors(self.choice, self.answers)

    def finish(self):
        self.good_answers = self.get_errors()
        return not self.good_answers

    def to_json(self):
        q = self.question
        choice = self.choice
        resp = {
            "descs": [desc.to_json() for desc in q.descs],
            "choice": self.choice,
            "answers_type": q.answers_type.name
        }

        if self.good_answers:
            resp["good_answers"] = self.good_answers

        if q.answers_type.allow:
            resp["answers"] = {v: k.text for v, k in self.answers.items()}

        return resp


class Game(object):

    quiz = None
    questions = None
    end = False
    good_question = []
    len_questions = 0

    _pointer = 0

    def __init__(self, key):
        self.quiz = conf.quizzes[key]

        self.questions = [GameQuestion(q) for q in self.quiz.questions]
        self.len_questions = len(self.questions)
        shuffle(self.questions)

    def get_game_question(self):
        return self.questions[self._pointer]

    def change_pointer(self, pointer):
        if pointer in range(self.len_questions):
            self._pointer = pointer
            return True
        else:
            return False

    def finish(self):
        self.end = True
        self.good_question = [q.finish() for q in self.questions]


    @property
    def pointer(self):
        return self._pointer

    def to_json(self):
        json = self.get_game_question().to_json()
        json.update({
            "pointer": self._pointer,
            "len_questions": self.len_questions,
            "end": self.end
        })

        if self.end:
            json["good_question"] = self.good_question

        return json
