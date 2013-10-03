import unittest
import os

from lxml import etree

from quizfactory import models

path = os.path.dirname(__file__)


def get_path(name):
    return os.path.join(path, "fixtures", name)


class TestXML(unittest.TestCase):

    def test_quiz(self):
        filename = get_path("quiz.xml")
        quiz = models.Quiz.load_from_file(filename)

        self.assertIsInstance(quiz.desc, models.Description)
        self.assertEqual(len(quiz.questions), 2)

        q = quiz.questions[0]

        self.assertEqual(len(q.answers), 3)
        self.assertEqual(len(q.descs), 3)

    def test_description(self):
        xml_str = '<desc syntax="C" name="file.c">main(){}</desc>'
        desc = models.Description.from_xml(etree.fromstring(xml_str))

        self.assertEqual(desc.text, "main(){}")
        self.assertEqual(desc.syntax, "c")
        self.assertEqual(desc.name, "file.c")

    def test_answer(self):

        def answer_factory(tag):
            node = etree.fromstring("<{0}>Lorem</{0}>".format(tag))
            return models.Answer.from_xml(node)

        self.assertFalse(answer_factory("false").is_correct)
        self.assertTrue(answer_factory("true").is_correct)
        self.assertEqual(answer_factory("true").text, "Lorem")

        self.assertRaises(KeyError, lambda: answer_factory("wrong"))

    def test_question(self):

        filename = get_path("question.xml")

        with open(filename) as f:
            node = etree.fromstring(f.read())

        q = models.Question.from_xml(node)

        self.assertEqual(len(q.answers), 2)
        self.assertEqual(len(q.descs), 2)
        self.assertEqual(q.answer_type, 'checkbox')


class TestDescription(unittest.TestCase):

    def test_markdown(self):

        from markdown import markdown

        text = """
Super Title
=====
Super Description Text
            """
        mark = markdown(text)

        self.assertEquals(models.Description(text).html, mark)
        self.assertEquals(models.Description(text, "markdown").html, mark)

    def test_syntax(self):

        from pygments import highlight
        from pygments.lexers import CLexer
        from pygments.formatters import HtmlFormatter

        c_code = """
            int main(int argc, char** argv){
                printf(\"test\\n\"); 
            }
            """

        html = highlight(c_code, CLexer(), HtmlFormatter())

        self.assertEquals(models.Description(c_code, "c").html, html)
