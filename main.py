#!flask/bin/python
from flask import Flask, make_response, abort, jsonify, request
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

from video_poker import Card, Deck, Hand, Payout
deck = Deck()

app = Flask(__name__)
CORS(app)

@app.route('/api/games', methods=['GET'])
def getGames():
    games = []
    gamesRef = db.collection('games').list_documents()
    for gameRef in gamesRef:
        game = gameRef.get().to_dict()
        game['id'] = gameRef.id
        games.append(game)
    return jsonify(games)

@app.route('/api/games', methods=['POST'])
def createGame():
    game = {
        'hand': request.json.get('hand', []),
        'payout': request.json.get('payout', Payout()),
        'bankroll': request.json.get('bankroll', 1000),
        'denomination': request.json.get('denomination', 1),
        'numCredits': request.json.get('numCredits', 5),
        'outcome': None,
        'creditsWon': 0,
        'inPlay': False
    }
    gameRef = db.collection('games').document()
    return jsonify({
        'id': gameRef.id,
        'update_time': gameRef.set(game).update_time.seconds,
        'game': game
    }), 201

@app.route('/api/games/<string:userId>', methods=['GET'])
def getGame(userId):
    gameRef = db.document('games/' + userId)
    game = gameRef.get().to_dict()
    if game is None:
        return ''
    return jsonify(game)

@app.route('/api/games/<string:userId>', methods=['POST'])
def startNewGame(userId):
    game = {
        'hand': request.json.get('hand', []),
        'payout': request.json.get('payout', Payout()),
        'bankroll': request.json.get('bankroll', 1000),
        'denomination': request.json.get('denomination', 1),
        'numCredits': request.json.get('numCredits', 5),
        'outcome': None,
        'creditsWon': 0,
        'inPlay': False
    }
    gameRef = db.collection('games').document(userId)
    return jsonify({
        'id': gameRef.id,
        'update_time': gameRef.set(game).update_time.seconds,
        'game': game
    }), 200

@app.route('/api/games/<string:userId>', methods=['DELETE'])
def deleteGame(userId):
    gameRef = db.document('games/' + userId)
    return jsonify({
        'time_deleted': gameRef.delete().seconds
    })

@app.route('/api/games/<string:userId>/draw', methods=['POST'])
def draw(userId):
    gameRef = db.document('games/' + userId)
    game = gameRef.get().to_dict()

    # error checking
    if game is None:
        return 'Game ' + userId + ' not found', 404
    game['numCredits'] = request.json.get('numCredits', game['numCredits'])
    game['denomination'] = request.json.get('denomination', game['denomination'])
    game['payout'] = request.json.get('payout', game['payout'])
    if game['bankroll'] < game['numCredits'] * game['denomination']:
        return 'Bankroll less than selected bet', 403

    # proceed with play
    game['bankroll'] -= game['numCredits'] * game['denomination']
    game['hand'] = deck.newHand()
    game['outcome'] = Hand(game['hand']).outcome()
    game['inPlay'] = True
    game['creditsWon'] = 0

    # update state in DB
    gameRef.update(game)

    # return state of the game
    return jsonify(game)

@app.route('/api/games/<string:userId>/redraw', methods=['POST'])
def redraw(userId):
    gameRef = db.document('games/' + userId)
    game = gameRef.get().to_dict()

    # error checking
    if game is None:
        return 'Game ' + userId + ' not found', 404
    if not game['hand']:
        return 'Hand is empty', 403
    hand = request.json.get('hand')
    if hand is None or not isinstance(hand, list):
        return 'Must pass hand', 403

    # db hand is source of truth - use payload hand for holding purposes only
    for i in range(5):
        game['hand'][i]['held'] = hand[i]['held']

    # proceed with play
    game['hand'] = deck.drawCards(game['hand'])
    game['outcome'] = Hand(game['hand']).outcome()
    game['creditsWon'] =   game['numCredits'] \
                         * game['denomination'] \
                         * game['payout'].get(game['outcome'], 0)
    game['bankroll'] += game['creditsWon']
    game['inPlay'] = False

    # update state in DB
    gameRef.update(game)

    # return state of the game
    return jsonify(game)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'})), 404

if __name__ == '__main__':
    app.run(debug=True)
