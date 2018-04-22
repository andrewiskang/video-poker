#!flask/bin/python
from flask import Flask, make_response, abort, jsonify
from video_poker2 import Card, Deck, Hand, Payout

app = Flask(__name__)

games = [{"id": 0,
          "deck": [],
          "hand": [],
          "payout": {"Royal Flush": 800,
                     "Straight Flush": 50,
                     "Four of a Kind": 25,
                     "Full House": 9,
                     "Flush": 6,
                     "Straight": 4,
                     "Three of a Kind": 3,
                     "Two Pair": 2,
                     "Jacks or Better": 1},
          "bankroll": 0,
          "num_credits": 5,
          "denomination": .25,
          "has_redrawn": False}]

@app.route("/")
def index():
    return "Video Poker!"

@app.route("/api/v1.0/games", methods=["GET"])
def get_games():
    return jsonify({'games' : games})

@app.route("/api/v1.0/games/<int:game_id>", methods=["GET"])
def get_game(game_id):
    game = [game for game in games if game["id"] == game_id]
    if len(game) == 0:
        abort(404)
    return jsonify({'game' : game[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error" : "Not found"})), 404

@app.route("/api/v1.0/games", methods=["POST"])
def create_game():
    if not request.json or not "payout" in request.json:
        abort(400)
    game = {
        "id": games[-1]["id"] + 1,
        "deck": request.json.get("deck", []),
        "hand": [],
        "payout": request.json["payout"],
        "bankroll": request.json.get("bankroll", 1000),
        "num_credits": request.json["num_credits"],
        "denomination": request.json["denomination"],
        "has_redrawn": False
    }
    games.append(game)
    return jsonify({"game": game}), 201

@app.route("/api/v1.0/games/<int:game_id>", methods=["DELETE"])
def delete_game(game_id):
    game = [game for game in games if game["id"] == game_id]
    if len(game) == 0:
        abort(404)
    games.remove(game[0])
    return jsonify({"success": True}), 204

@app.route("/api/v1.0/games/<int:game_id>/play)", methods=["PUT"])
def play(game_id):
    # deals a new hand or redraws certain cards based on has_redrawn
    game = [game for game in games if game["id"] == game_id]
    if len(game) == 0:
        abort(404)
    if not request.json:
        abort(400)
    hold_indices = request.json.get("hold_indices", [])
    for i in hold_indices:
        if i not in range(5):
            abort(400)

    num_credits = game[0]["num_credits"]
    denomination = game[0]["denomination"]
    payout = game[0]["payout"]
    if game[0]["has_redrawn"]:
        game[0]["bankroll"] -= num_credits * denomination
        game[0]["deck"] = Deck.new_deck()
        game[0]["hand"] = game[0]["deck"].draw_cards()
        game[0]["has_redrawn"] = False
    else:
        game[0]["hand"] = game[0]["deck"].draw_cards(game[0]["hand"], hold_indices)
        outcome = Hand(game[0]["hand"]).outcome()
        credits_won = payout.table[outcome] * num_credits
        game[0]["bankroll"] += credits_won * denomination
        game[0]["has_redrawn"] = True

    return jsonify({"success": True,
                    "game": game[0]}), 200


if __name__ == "__main__":
    app.run(debug=True)
