from lxml import etree


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
    name = ""

    def __init__(self, text, syntax=None, name=None):
        self.text = text

        if syntax:
            # todo - render syntax to HTML
            self.syntax = syntax

        if name:
            self.name = name

    @classmethod
    def from_xml(cls, node):
        return cls(node.text, node.get("syntax"), node.get("name"))

    def __str__(self):
        return "Description({}, syntax={}, name={}}".format(self.text[:20],
                                                            self.syntax,
                                                            self.name)


class Question(BaseModel):

    """ Question - has many descriptions """

    descs = None
    answers = None
    answers_type = "radio"

    @classmethod
    def from_xml(cls, node):
        q = cls()

        q.descs = [Description.from_xml(c) for c in node.iterfind("desc")]

        ans = node.find("answers")
        answer_type = ans.get("type")
        if answer_type:
            q.answer_type = answer_type
        q.answers = [Answer.from_xml(c) for c in ans.iterfind("true")]
        q.answers += [Answer.from_xml(c) for c in ans.iterfind("false")]
        # | operator in lxml's xpath doesn't work :/

        return q


class Quiz(BaseModel):

    """Quiz Model"""
    desc = None
    questions = None
    config = None

    @staticmethod
    def load_from_file(filename):

        with open(filename) as f:
            tree = etree.parse(f)

        quiz = Quiz()
        quiz.desc = Description.from_xml(tree.find("desc"))
        quiz.questions = [Question.from_xml(c) for c in
                          tree.iterfind("questions/q")]

        return quiz
