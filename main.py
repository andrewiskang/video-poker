#!flask/bin/python
from flask import Flask, make_response, abort, jsonify, request

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

from video_poker import Card, Deck, Hand, Payout

app = Flask(__name__)

@app.route('/')
def index():
    return 'Video Poker!'

@app.route('/api/games', methods=['POST'])
def createGame():
    game = {
        'hand': request.json.get('hand', []),
        'payout': request.json.get('payout', Payout()),
        'bankroll': request.json.get('bankroll', 1000),
        'denomination': request.json.get('denomination', 1)
    }
    gameRef = db.collection('games').document()
    return jsonify({
        'id': gameRef.id,
        'update_time': gameRef.set(game).update_time.seconds,
        'game': game
    }), 201

@app.route('/api/games/<string:gameId>', methods=['GET'])
def getGame(gameId):
    gameRef = db.document('games/'+gameId)
    return jsonify({
        'game' : gameRef.get().to_dict()
    })

@app.route('/api/games/<string:gameId>', methods=['DELETE'])
def deleteGame(gameId):
    gameRef = db.document('games/'+gameId)
    return jsonify({
        'time_deleted': gameRef.delete().seconds
    })

# @app.route('/api/games', methods=['GET'])
# def getGames():
#     return jsonify({'games' : games})


# @app.route('/api/games/<string:gameId>', methods=['GET'])
# def getGame(gameId):
#     game = [game for game in games if game['id'] == gameId]
#     if len(game) == 0:
#         abort(404)
#     hand = Hand(game[0]['hand'])
#     outcome = hand.outcome()
#     return jsonify({'hand': hand,
#                     'outcome': outcome})

# @app.route('/api/games/<string:gameId>/draw', methods=['GET'])
# def draw(gameId):
#     # deals a new hand or redraws certain cards based on has_redrawn
#     game = [game for game in games if game['id'] == gameId]

#     # error checking
#     if len(game) == 0:
#         abort(404)
#     if not request.json:
#         abort(400)
#     hold_indices = request.json.get('hold_indices', [])
#     for i in hold_indices:
#         if i not in range(5):
#             abort(400)

#     # determine current stage of the game. if already redrawn, start a new game
#     # otherwise redraw based on the hold_indices
#     num_credits = game[0]['num_credits']
#     denomination = game[0]['denomination']
#     payout = Payout(game[0]['payout'])
#     outcome = ''
#     if game[0]['has_redrawn'] or game[0]['hand'] == []:
#         # check if bankroll is large enough to place bet
#         if game[0]['bankroll'] < num_credits * denomination:
#             return jsonify({'success': False,
#                             'reason': 'bankroll less than selected bet'}), 403
#         # otherwise place bet, shuffle deck, and draw new hand
#         # to ensure deck contains all cards, we re-initialize a new deck
#         game[0]['bankroll'] -= num_credits * denomination
#         game[0]['deck'] = Deck.new_deck()
#         game[0]['hand'] = game[0]['deck'].draw_cards()
#         outcome = Hand(game[0]['hand']).outcome()
#         game[0]['has_redrawn'] = False
#     else:
#         # continue with the game, redrawing select cards based off hold_indices
#         # once cards are redrawn, determine outcome and pay user accordingly
#         deck = Deck(game[0]['deck'])
#         game[0]['hand'] = deck.draw_cards(game[0]['hand'], hold_indices)
#         game[0]['deck'] = deck
#         outcome = Hand(game[0]['hand']).outcome()
#         credits_won = payout[outcome] * num_credits
#         game[0]['bankroll'] += credits_won * denomination
#         game[0]['has_redrawn'] = True

#     # return current stage of the game (has_redrawn),
#     return jsonify({'success': True,
#                     'hand': game[0]['hand'],
#                     'outcome': outcome,
#                     'has_redrawn': game[0]['has_redrawn'],
#                     'bankroll': game[0]['bankroll']}), 200

# @app.route('/api/games/<string:gameId>/draw', methods=['GET'])
# def draw_or_redraw(gameId):
#     # deals a new hand or redraws certain cards based on has_redrawn
#     game = [game for game in games if game['id'] == gameId]

#     # error checking
#     if len(game) == 0:
#         abort(404)
#     if not request.json:
#         abort(400)
#     hold_indices = request.json.get('hold_indices', [])
#     for i in hold_indices:
#         if i not in range(5):
#             abort(400)

#     # determine current stage of the game. if already redrawn, start a new game
#     # otherwise redraw based on the hold_indices
#     num_credits = game[0]['num_credits']
#     denomination = game[0]['denomination']
#     payout = Payout(game[0]['payout'])
#     outcome = ''
#     if game[0]['has_redrawn'] or game[0]['hand'] == []:
#         # check if bankroll is large enough to place bet
#         if game[0]['bankroll'] < num_credits * denomination:
#             return jsonify({'success': False,
#                             'reason': 'bankroll less than selected bet'}), 403
#         # otherwise place bet, shuffle deck, and draw new hand
#         # to ensure deck contains all cards, we re-initialize a new deck
#         game[0]['bankroll'] -= num_credits * denomination
#         game[0]['deck'] = Deck.new_deck()
#         game[0]['hand'] = game[0]['deck'].draw_cards()
#         outcome = Hand(game[0]['hand']).outcome()
#         game[0]['has_redrawn'] = False
#     else:
#         # continue with the game, redrawing select cards based off hold_indices
#         # once cards are redrawn, determine outcome and pay user accordingly
#         deck = Deck(game[0]['deck'])
#         game[0]['hand'] = deck.draw_cards(game[0]['hand'], hold_indices)
#         game[0]['deck'] = deck
#         outcome = Hand(game[0]['hand']).outcome()
#         credits_won = payout[outcome] * num_credits
#         game[0]['bankroll'] += credits_won * denomination
#         game[0]['has_redrawn'] = True

#     # return current stage of the game (has_redrawn),
#     return jsonify({'success': True,
#                     'hand': game[0]['hand'],
#                     'outcome': outcome,
#                     'has_redrawn': game[0]['has_redrawn'],
#                     'bankroll': game[0]['bankroll']}), 200

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'})), 404

if __name__ == '__main__':
    app.run(debug=True)
