from quizfactory import app, conf
from flask import render_template


@app.fine_route()
def get_quiz(quiz_id):
    try:
        quiz = conf.quizzes[quiz_id]
    except IndexError:
        return 404
    else:
        return render_template("quiz.html", quiz=quiz)


@app.fine_route()
def put_quiz(quiz_id):
    pass


@app.fine_route()
def delete_quiz(quiz_id):
    pass
