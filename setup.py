#!/usr/bin/env python

from setuptools import setup, find_packages

install_requires = [
    'Flask==0.10.1',
    'Pygments==1.6',
    'lxml==3.2.3',
    'Markdown==2.3.1'
]

setup(
    name='QuizFactory',
    version='0.3',
    description='Generate site with quizzes',
    author='Marek Piechula',
    author_email='marpiechula@gmail.com',
    url='https://github.com/firemark/quizFactory',
    packages=find_packages(),
    license="MIT",
    test_suite="quizfactory.tests",
    install_requires=install_requires,
)
