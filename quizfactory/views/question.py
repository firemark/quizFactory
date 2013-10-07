from quizfactory import app
from quizfactory.models import Game
from flask import session, jsonify

games = {}

@app.fine_route()
def get_question(quiz_id):
    global games
    try:
        game = games[session[quiz_id]]
    except KeyError:
        game = Game(quiz_id)
        id_game = id(game)
        games[id_game] = game
        session[quiz_id] = id_game

    return jsonify(**game.get_game_question().to_json())


@app.fine_route()
def post_question(quiz_id):
    pass
