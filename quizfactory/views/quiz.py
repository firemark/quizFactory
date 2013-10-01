from quizfactory import app


@app.fine_route()
def get_quiz(quiz):
    return "Hello %s!" % quiz


@app.fine_route()
def put_quiz(quiz):
    pass


@app.fine_route()
def delete_quiz(quiz):
    pass
