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
        random_str = str(random()).encode('utf-8')
        self.answers = {  # hash: answer
            sha1(random_str + a.text.encode('utf-8')).hexdigest()[:8]: a
            for a in q.answers
        }

        self.choice = self.question.answers_type.set_choice()

    def get_errors(self):
        """Return list of errors (only keys)"""
        return self.question.answers_type.get_errors(self.choice, self.answers)

    def to_json(self, end):
        q = self.question
        choice = self.choice
        resp = {
            "descs": [desc.to_json() for desc in q.descs],
            "choice": choice,
            "answers_type": q.answers_type.name
        }

        if q.answers_type.allow or end:
            if end:
                d = {v: {"text": k.text, "is_correct": k.is_correct}
                     for v, k in self.answers.items()}
            else:
                d = {v: {"text": k.text} for v, k in self.answers.items()}

            resp["answers"] = d

        return resp


class Game(object):

    quiz = None
    questions = None
    end = False
    good_question = []  # question #0 -> True, question #1 -> False...
    len_good_questions = 0
    len_questions = 0

    _pointer = 0

    def __init__(self, key, randoms=True):
        self.quiz = conf.quizzes[key]

        self.questions = [GameQuestion(q) for q in self.quiz.questions]
        self.len_questions = len(self.questions)
        if randoms:
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
        self.good_question = [not bool(q.get_errors()) for q in self.questions]
        self.len_good_questions = sum(self.good_question)  # True = 1 <3

    @property
    def pointer(self):
        return self._pointer

    @classmethod
    def unserialize(cls, json):
        game = cls(json.question_key, False)

    def to_json(self):
        json = self.get_game_question().to_json(self.end)
        json.update({
            "pointer": self._pointer,
            "len_questions": self.len_questions,
            "end": self.end
        })

        if self.end:
            json.update({
                "good_question": self.good_question,
                "len_good_questions": self.len_good_questions
            })

        return json
