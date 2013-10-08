from quizfactory import app
from quizfactory.models import Game
from flask import session, jsonify, request

games = {}


def get_game_from_session(quiz_id):
    global games
    return games[session[quiz_id]]


@app.fine_route()
def get_game(quiz_id):
    try:
        game = get_game_from_session(quiz_id)
    except KeyError:
        return jsonify(error="quiz not found"), 404

    return jsonify(**game.to_json())


@app.fine_route()
def post_game(quiz_id):
    global games
    try:
        game = get_game_from_session(quiz_id)
    except KeyError:
        game = Game(quiz_id)
        id_game = id(game)
        games[id_game] = game
        session[quiz_id] = id_game


    return jsonify(**game.to_json())


@app.fine_route()
def put_game(quiz_id):
    try:
        game = get_game_from_session(quiz_id)
    except KeyError:
        return jsonify(error="quiz not found"), 404

    data = request.json
    print(data)
    choice = data.get("choice")
    pointer = data.get("pointer")

    if pointer is not None:
        game.change_pointer(pointer)

    if choice is not None:
        game.get_game_question().choice = choice

    return jsonify(**game.to_json())


@app.fine_route()
def delete_game(quiz_id):
    pass
