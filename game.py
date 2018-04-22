#!flask/bin/python
from flask import Flask, make_response, abort, jsonify, request
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

@app.route("/api/v1.0/games", methods=["POST"])
def create_game():
    if not request.json or not "denomination" in request.json:
        abort(400)
    game = {
        "id": games[-1]["id"] + 1,
        "deck": request.json.get("deck", Deck.new_deck()),
        "hand": [],
        "payout": request.json.get("payout", Payout.default()),
        "bankroll": request.json.get("bankroll", 1000),
        "num_credits": request.json.get("num_credits", 5),
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

@app.route("/api/v1.0/games/<int:game_id>/play", methods=["GET"])
def show_play(game_id):
    game = [game for game in games if game["id"] == game_id]
    if len(game) == 0:
        abort(404)
    hand = Hand(game[0]["hand"])
    outcome = hand.outcome()
    return jsonify({"hand": hand,
                    "outcome": outcome})

@app.route("/api/v1.0/games/<int:game_id>/play", methods=["PUT"])
def draw_or_redraw(game_id):
    # deals a new hand or redraws certain cards based on has_redrawn
    game = [game for game in games if game["id"] == game_id]

    # error checking
    if len(game) == 0:
        abort(404)
    if not request.json:
        abort(400)
    hold_indices = request.json.get("hold_indices", [])
    for i in hold_indices:
        if i not in range(5):
            abort(400)

    # determine current stage of the game. if already redrawn, start a new game
    # otherwise redraw based on the hold_indices
    num_credits = game[0]["num_credits"]
    denomination = game[0]["denomination"]
    payout = Payout(game[0]["payout"])
    outcome = ""
    if game[0]["has_redrawn"] or game[0]["hand"] == []:
        # check if bankroll is large enough to place bet
        if game[0]["bankroll"] < num_credits * denomination:
            return jsonify({"success": False,
                            "reason": "bankroll less than selected bet"}), 403
        # otherwise place bet, shuffle deck, and draw new hand
        # to ensure deck contains all cards, we re-initialize a new deck
        game[0]["bankroll"] -= num_credits * denomination
        game[0]["deck"] = Deck.new_deck()
        game[0]["hand"] = game[0]["deck"].draw_cards()
        outcome = Hand(game[0]["hand"]).outcome()
        game[0]["has_redrawn"] = False
    else:
        # continue with the game, redrawing select cards based off hold_indices
        # once cards are redrawn, determine outcome and pay user accordingly
        deck = Deck(game[0]["deck"])
        game[0]["hand"] = deck.draw_cards(game[0]["hand"], hold_indices)
        game[0]["deck"] = deck
        outcome = Hand(game[0]["hand"]).outcome()
        credits_won = payout[outcome] * num_credits
        game[0]["bankroll"] += credits_won * denomination
        game[0]["has_redrawn"] = True

    # return current stage of the game (has_redrawn),
    return jsonify({"success": True,
                    "hand": game[0]["hand"],
                    "outcome": outcome,
                    "has_redrawn": game[0]["has_redrawn"],
                    "bankroll": game[0]["bankroll"]}), 200

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error" : "Not found"})), 404

if __name__ == "__main__":
    app.run(debug=True)
