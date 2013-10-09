#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='QuizFactory',
    version='0.2',
    description='Generate site with quizzes',
    author='Marek Piechula',
    author_email='marpiechula@gmail.com',
    url='https://github.com/firemark/quizFactory',
    packages=find_packages(),
    license="MIT",
    test_suite="quizfactory.tests",
    install_requires=['flask', 'pygments', 'lxml', 'markdown'],
)
