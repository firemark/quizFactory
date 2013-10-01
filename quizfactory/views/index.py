from quizfactory import app


@app.fine_route()
def get_index():
    return 'Hello World!'