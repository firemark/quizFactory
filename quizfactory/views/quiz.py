from quizfactory import app, conf
from flask import render_template


@app.fine_route()
def get_quiz(quiz_id):
    try:
        quiz = conf.quizzes[quiz_id]
    except KeyError:
        return render_template("quiz_not_found.html"), 404
    else:
        return render_template("quiz.html", quiz=quiz, quiz_id=quiz_id)
