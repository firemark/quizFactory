from quizfactory import app
from quizfactory.models import Game
from flask import session, jsonify, request
import pickle


def load_game(quiz_id):
    try:
        return session[quiz_id]
    except KeyError:
        return None


def save_game(quiz_id, game):
    session[quiz_id] = game
    session.modified = True


@app.fine_route()
def get_game(quiz_id):
    game = load_game(quiz_id)
    if not game:
        return jsonify(error="quiz not found"), 404

    return jsonify(**game.to_json())


@app.fine_route()
def post_game(quiz_id):
    game = load_game(quiz_id)
    if not game:
        game = Game(quiz_id)
        save_game(quiz_id, game)

    return jsonify(**game.to_json())


@app.fine_route()
def put_game(quiz_id):
    game = load_game(quiz_id)
    if not game:
        return jsonify(error="quiz not found"), 404

    data = request.json

    choice = data.get("choice")
    pointer = data.get("pointer")

    if data.get("finish"):
        game.finish()
    elif pointer is not None and pointer != game.pointer:
        game.change_pointer(pointer)
    elif choice is not None and not game.end:
        gq = game.get_game_question()
        if gq.question.answers_type.is_valid(choice):
            gq.choice = choice
        else:
            return jsonify(
                error="choice object is not a valid object to this answer"
            ), 403

    save_game(quiz_id, game)
    return jsonify(**game.to_json())


@app.fine_route()
def delete_game(quiz_id):
    try:
        del session[quiz_id]
    except KeyError:
        return jsonify(error="quiz not found"), 404

    return jsonify(), 200
