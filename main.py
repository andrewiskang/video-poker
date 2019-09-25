#!flask/bin/python
from flask import Flask, make_response, abort, jsonify, request

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

from video_poker import Card, Deck, Hand, Payout
deck = Deck()

app = Flask(__name__)

@app.route('/')
def index():
    return 'Video Poker!'

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
        'numCredits': request.json.get('numCredits', 5)
    }
    gameRef = db.collection('games').document()
    return jsonify({
        'id': gameRef.id,
        'update_time': gameRef.set(game).update_time.seconds,
        'game': game
    }), 201

@app.route('/api/games/<string:gameId>', methods=['GET'])
def getGame(gameId):
    gameRef = db.document('games/' + gameId)
    game = gameRef.get().to_dict()
    if game is None:
        return 'Game ' + gameId + ' not found', 404
    return jsonify(game)

@app.route('/api/games/<string:gameId>', methods=['DELETE'])
def deleteGame(gameId):
    gameRef = db.document('games/' + gameId)
    return jsonify({
        'time_deleted': gameRef.delete().seconds
    })

@app.route('/api/games/<string:gameId>/draw', methods=['POST'])
def draw(gameId):
    gameRef = db.document('games/' + gameId)
    game = gameRef.get().to_dict()

    # error checking
    if game is None:
        return 'Game ' + gameId + ' not found', 404
    game['numCredits'] = request.json.get('numCredits', game['numCredits'])
    game['denomination'] = request.json.get('denomination', game['denomination'])
    if game['bankroll'] < game['numCredits'] * game['denomination']:
        return 'Bankroll less than selected bet', 403

    # proceed with play
    game['bankroll'] -= game['numCredits'] * game['denomination']
    game['hand'] = deck.newHand()
    game['outcome'] = Hand(game['hand']).outcome()

    # update state in DB
    gameRef.update({
        'bankroll': game['bankroll'],
        'hand': game['hand'],
        'denomination': game['denomination'],
        'numCredits': game['numCredits']
    })

    # return state of the game
    return jsonify(game)

@app.route('/api/games/<string:gameId>/redraw', methods=['POST'])
def redraw(gameId):
    gameRef = db.document('games/' + gameId)
    game = gameRef.get().to_dict()

    # error checking
    if game is None:
        return 'Game ' + gameId + ' not found', 404
    if not game['hand']:
        return 'Hand is empty', 403
    game['holdIndices'] = request.json.get('holdIndices')
    if game['holdIndices'] is None or not isinstance(game['holdIndices'], list):
        return 'Must pass card indices to hold as an array', 400

    # proceed with play
    game['hand'] = deck.drawCards(game['hand'], game['holdIndices'])
    game['outcome'] = Hand(game['hand']).outcome()
    game['creditsWon'] =   game['numCredits'] \
                         * game['denomination'] \
                         * game['payout'].get(game['outcome'], 0)
    game['bankroll'] += game['creditsWon']

    # update state in DB
    gameRef.update({
        'bankroll': game['bankroll'],
        'hand': game['hand']
    })

    # return state of the game
    return jsonify(game)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Not found'})), 404

if __name__ == '__main__':
    app.run(debug=True)
