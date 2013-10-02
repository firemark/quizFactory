from flask import Flask
from quizfactory import conf


class FiremarkFlask(Flask):

    """:D"""

    def fine_route(self, **options):
        """ add view using function name with url from config """

        def decorator(f):
            endpoint = options.pop('endpoint', f.__name__),
            method, name = f.__name__.split('_', 1)
            options["methods"] = [method.upper()]
            self.add_url_rule(conf.urls[name], endpoint, f, **options)
            return f

        return decorator

app = FiremarkFlask("quizFactory")
