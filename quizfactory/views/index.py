from quizfactory import app, conf
from flask import render_template


@app.fine_route()
def get_index():
    return render_template('index.html', quizzes=conf.quizzes)
