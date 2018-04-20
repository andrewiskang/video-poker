#!flask/bin/python
from flask import Flask, make_response, abort, jsonify

app = Flask(__name__)

games = [{"id": 0,
          "deck": [],
          "hand": [],
          "payout": {},
          "bankroll": 0,
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
    return jsonify({"result": True})

if __name__ == "__main__":
    app.run(debug=True)
