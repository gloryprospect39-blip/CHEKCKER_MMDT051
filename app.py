from __future__ import annotations

import os

from flask import Flask, jsonify, render_template, request

from agent import HeuristicAgent, MinimaxAgent, RandomAgent
from checkers import BLACK, WHITE, Board, Move

app = Flask(__name__)

HUMAN_COLOR = BLACK
AI_COLOR = WHITE


def reset_board():
    global board
    board = Board(turn=HUMAN_COLOR)


reset_board()
agents = {
    "easy": RandomAgent(AI_COLOR),
    "medium": HeuristicAgent(AI_COLOR),
    "hard": MinimaxAgent(AI_COLOR, depth=3),
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/state')
def api_state():
    return jsonify({
        'board': board.board,
        'turn': board.turn,
        'winner': board.winner(),
    })


@app.route('/api/reset', methods=['POST'])
def api_reset():
    reset_board()
    return jsonify({'board': board.board, 'turn': board.turn, 'winner': board.winner()})


@app.route('/api/move', methods=['POST'])
def api_move():
    global board
    if board.winner() is not None:
        return jsonify({'error': 'Game is already over'}), 409
    if board.turn != HUMAN_COLOR:
        return jsonify({'error': 'It is not the human turn'}), 400

    payload = request.get_json(force=True, silent=True) or {}
    start = tuple(payload.get('from', (0, 0)))
    end = tuple(payload.get('to', (0, 0)))
    if not start or not end:
        return jsonify({'error': 'Move coordinates missing'}), 400

    move = Move(start, end)
    legal = board.legal_moves_for(board.turn)
    if move not in legal:
        return jsonify({'error': 'Illegal move'}), 400

    board = board.apply_move(move)
    return jsonify({'board': board.board, 'turn': board.turn, 'winner': board.winner()})


@app.route('/api/ai', methods=['POST'])
def api_ai():
    global board
    if board.winner() is not None:
        return jsonify({'move': None, 'winner': board.winner()})
    if board.turn != AI_COLOR:
        return jsonify({'move': None, 'turn': board.turn, 'winner': board.winner()})

    payload = request.get_json(force=True, silent=True) or {}
    difficulty = payload.get('difficulty', 'medium')
    agent = agents.get(difficulty, agents['medium'])
    move = agent.select_move(board)
    if move is None:
        return jsonify({'move': None, 'board': board.board, 'turn': board.turn, 'winner': board.winner()})
    board = board.apply_move(move)
    return jsonify({'move': {'from': move.from_pos, 'to': move.to_pos}, 'board': board.board, 'turn': board.turn, 'winner': board.winner()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
