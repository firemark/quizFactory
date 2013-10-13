try:
    str_type = basestring
except NameError:
    str_type = str

__all__ = ["get_answer_type", "get_all_answer_types"]

types = {}


def get_answer_type(name):
    return types[name]


def get_all_answer_types():
    return types.values()


def register(cls):
    global types
    name = cls.__name__.split("Type")[0].lower()

    cls.name = name
    types[name] = cls

    return cls


class AbstractType(object):

    allow = True

    @staticmethod
    def get_good_answers(answers):
        return [k for k, v in answers.items() if v.is_correct]

    @classmethod
    def get_errors(cls, choice, answers):
        """Return list of errors (only keys)"""
        raise NotImplemented("get_errors")

    @classmethod
    def is_valid(cls, input):
        """parse input from request"""
        return isinstance(input, str_type) and len(input) == 8

    @staticmethod
    def set_choice():
        """set default empty choice"""
        return ""


@register
class RadioType(AbstractType):

    @classmethod
    def get_errors(cls, choice, answers):
        good_answers = cls.get_good_answers(answers)
        return [choice] if choice not in good_answers else []


@register
class CheckboxType(AbstractType):

    @classmethod
    def get_errors(cls, choice, answers):
        good_answers = cls.get_good_answers(answers)
        return list(set(good_answers) - set(choice))

    @staticmethod
    def set_choice():
        return []  # list of selected answers

    @classmethod
    def is_valid(cls, input):
        if not isinstance(input, list):
            return False

        for value in input:
            if not super(CheckboxType, cls).is_valid(value):
                return False

        return True


@register
class TextType(AbstractType):

    allow = False

    @classmethod
    def get_errors(cls, choice, answers):
        choice = choice.strip()
        gen = (v.text.strip() for v in answers.values() if v.is_correct)
        return cls.get_good_answers(answers) if choice not in gen else []

    @classmethod
    def is_valid(cls, input):
        return isinstance(input, str_type)
