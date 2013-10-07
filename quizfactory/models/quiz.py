from lxml import etree

from markdown import markdown

from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
from pygments.formatters import HtmlFormatter

from quizfactory.utils import strip_indents
from .answer_types import get_answer_type

import os
from cgi import escape

__all__ = ['Answer', 'Quiz', 'Description', 'Question', 'Quiz']

formater = HtmlFormatter()


class BaseModel(object):

    @classmethod
    def from_xml(cls, node):
        raise NotImplementedError("load from xml not implemented")


class Answer(BaseModel):
    text = ""
    is_correct = False

    def __init__(self, text, is_correct=False):
        self.text = text
        self.is_correct = is_correct

    @classmethod
    def from_xml(cls, node):
        correct_str = node.tag

        if correct_str == 'false':
            is_correct = False
        elif correct_str == 'true':
            is_correct = True
        else:
            raise KeyError(correct_str)

        return cls(node.text, is_correct)

    def __str__(self):
        return "Answer({}, {})".format(self.is_correct, self.text)


class Description(BaseModel):
    text = ""
    syntax = "markdown"
    html = ""
    name = ""

    def __init__(self, text, syntax=None, name=None):
        self.text = strip_indents(text)
        lexer = None

        if name:
            self.name = name

        if syntax is not None:
            self.syntax = syntax.lower()
        elif self.name:
            try:
                lexer = get_lexer_for_filename(self.name)
            except ClassNotFound:
                pass
            else:
                self.syntax = lexer.aliases[0]

        if self.syntax == "markdown":
            self.html = markdown(self.text)
        else:
            try:
                lexer = lexer or get_lexer_by_name(self.syntax)
            except ClassNotFound:
                # do nothing - if html is empty then description is a raw text
                pass
            else:
                self.html = highlight(self.text, lexer, formater)

    @classmethod
    def from_xml(cls, node):
        return cls(node.text, node.get("syntax"), node.get("name"))

    def to_json(self):
        return {
            "syntax": self.syntax,
            "html": str(self),
            "name": self.name
        }

    def __repr__(self):
        return "Description(%s, %s)" % (self.name, self.syntax)

    def __str__(self):
        return self.html or "<pre>%s</pre>" % escape(self.text)


class Question(BaseModel):

    """ Question - has many descriptions """

    descs = None
    answers = None
    answers_type = None

    def __init__(self, answers_type=None):
        answers_type = answers_type or "radio"
        self.answers_type = get_answer_type(answers_type)

    @classmethod
    def from_xml(cls, node):

        ans = node.find("answers")
        q = cls(ans.get("type"))

        q.descs = [Description.from_xml(c) for c in node.iterfind("desc")]
        q.answers = [Answer.from_xml(c) for c in ans.iterfind("true")]
        q.answers += [Answer.from_xml(c) for c in ans.iterfind("false")]
        # | operator in lxml's xpath doesn't work :/

        return q


class Quiz(BaseModel):

    """Quiz Model"""
    filename = ""
    name = ""
    desc = None
    questions = None
    config = None

    @staticmethod
    def load_from_file(filename):

        with open(filename) as f:
            tree = etree.parse(f)

        quiz = Quiz()
        quiz.filename = os.path.split(filename)[-1]
        quiz.name = tree.find("name").text
        quiz.desc = Description.from_xml(tree.find("desc"))
        quiz.questions = [Question.from_xml(c) for c in
                          tree.iterfind("questions/q")]

        return quiz
