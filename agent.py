import random
from typing import Optional

from checkers import BLACK, WHITE, Board, Move, evaluate_board


class RandomAgent:
    def __init__(self, player: int = BLACK, seed: Optional[int] = None):
        self.player = player
        self.rng = random.Random(seed)

    def select_move(self, board: Board):
        legal = board.legal_moves_for(self.player)
        if not legal:
            return None
        return self.rng.choice(legal)

    def choose_move(self, board: Board):
        return self.select_move(board)


class HeuristicAgent:
    def __init__(self, player: int = BLACK):
        self.player = player

    def evaluate_move(self, board: Board, move: Move) -> float:
        next_board = board.apply_move(move)
        return evaluate_board(next_board, self.player)

    def select_move(self, board: Board):
        legal = board.legal_moves_for(self.player)
        if not legal:
            return None
        return max(legal, key=lambda move: self.evaluate_move(board, move))

    def choose_move(self, board: Board):
        return self.select_move(board)


class MinimaxAgent:
    def __init__(self, player: int = BLACK, depth: int = 3):
        self.player = player
        self.depth = depth
        self.nodes_evaluated = 0

    def evaluate_position(self, board: Board) -> float:
        return evaluate_board(board, self.player)

    def _minimax(self, board: Board, depth: int, alpha: float, beta: float, maximizing: bool) -> float:
        self.nodes_evaluated += 1
        winner = board.winner()
        if winner == self.player:
            return 100000 + depth
        if winner == (0 if self.player == BLACK else BLACK):
            return -100000 - depth
        if winner == 0:
            return 0
        if depth == 0:
            return self.evaluate_position(board)

        moves = board.legal_moves_for(BLACK if maximizing else WHITE)
        if not moves:
            return -100000 if maximizing else 100000

        if maximizing:
            best_score = float('-inf')
            for move in moves:
                next_board = board.apply_move(move)
                score = self._minimax(next_board, depth - 1, alpha, beta, False)
                best_score = max(best_score, score)
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
            return best_score

        best_score = float('inf')
        for move in moves:
            next_board = board.apply_move(move)
            score = self._minimax(next_board, depth - 1, alpha, beta, True)
            best_score = min(best_score, score)
            beta = min(beta, score)
            if alpha >= beta:
                break
        return best_score

    def select_move(self, board: Board):
        legal = board.legal_moves_for(self.player)
        if not legal:
            return None
        self.nodes_evaluated = 0
        best_move = legal[0]
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in legal:
            next_board = board.apply_move(move)
            score = self._minimax(next_board, self.depth - 1, alpha, beta, False)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)

        return best_move

    def choose_move(self, board: Board):
        return self.select_move(board)
