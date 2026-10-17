from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

BOARD_SIZE = 8
BLACK = 1
WHITE = -1
EMPTY = 0


def is_dark_square(row: int, col: int) -> bool:
    return (row + col) % 2 == 1


@dataclass(frozen=True)
class Move:
    from_pos: Tuple[int, int]
    to_pos: Tuple[int, int]
    captured: Tuple[Tuple[int, int], ...] = ()
    is_capture: bool = False

    def __iter__(self):
        yield self.from_pos
        yield self.to_pos

    def as_tuple(self):
        return (self.from_pos, self.to_pos, self.captured)


class Board:
    """A compact Myanmar Checkers board implementation."""

    def __init__(self, board: Optional[Sequence[Sequence[int]]] = None, turn: int = BLACK):
        self.board = self._clone_board(board) if board is not None else self.initial_board()
        self.turn = turn

    @staticmethod
    def initial_board() -> List[List[int]]:
        board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if not is_dark_square(row, col):
                    continue
                if row < 3:
                    board[row][col] = WHITE
                elif row > 4:
                    board[row][col] = BLACK
        return board

    @staticmethod
    def _clone_board(board: Sequence[Sequence[int]]) -> List[List[int]]:
        return [list(row) for row in board]

    def copy(self) -> "Board":
        return Board(self.board, self.turn)

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def get_piece(self, row: int, col: int) -> int:
        if not self.in_bounds(row, col):
            return EMPTY
        return self.board[row][col]

    def set_piece(self, row: int, col: int, value: int) -> None:
        if self.in_bounds(row, col):
            self.board[row][col] = value

    @staticmethod
    def _piece_color(value: int) -> int:
        if value == EMPTY:
            return 0
        return BLACK if value > 0 else WHITE

    @staticmethod
    def _piece_is_king(value: int) -> bool:
        return abs(value) == 2

    def _movement_directions(self, value: int) -> List[Tuple[int, int]]:
        if abs(value) == 2:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if value > 0:
            return [(-1, -1), (-1, 1)]
        return [(1, -1), (1, 1)]

    def _capture_sequences(self, board: Sequence[Sequence[int]], row: int, col: int, color: int, start: Tuple[int, int], captured: Tuple[Tuple[int, int], ...] = ()) -> List[Move]:
        piece = board[row][col]
        if piece == EMPTY:
            return []
        results: List[Move] = []
        for dr, dc in self._movement_directions(piece):
            mid_row = row + dr
            mid_col = col + dc
            end_row = row + 2 * dr
            end_col = col + 2 * dc
            if not (self.in_bounds(mid_row, mid_col) and self.in_bounds(end_row, end_col)):
                continue
            mid_piece = board[mid_row][mid_col]
            if mid_piece == EMPTY or self._piece_color(mid_piece) == color:
                continue
            if board[end_row][end_col] != EMPTY:
                continue
            next_board = [list(line) for line in board]
            next_board[row][col] = EMPTY
            next_board[mid_row][mid_col] = EMPTY
            next_board[end_row][end_col] = piece
            if not self._piece_is_king(piece) and ((piece > 0 and end_row == BOARD_SIZE - 1) or (piece < 0 and end_row == 0)):
                next_board[end_row][end_col] = piece * 2
            deeper = self._capture_sequences(next_board, end_row, end_col, color, start, captured + ((mid_row, mid_col),))
            if deeper:
                results.extend(deeper)
            else:
                results.append(Move(start, (end_row, end_col), captured=captured + ((mid_row, mid_col),), is_capture=True))
        return results

    def generate_moves(self, color: Optional[int] = None) -> List[Move]:
        active = self.turn if color is None else color
        captures = []
        simple = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece == EMPTY or self._piece_color(piece) != active:
                    continue
                for dr, dc in self._movement_directions(piece):
                    mid_row = row + dr
                    mid_col = col + dc
                    if self.in_bounds(mid_row, mid_col) and self.in_bounds(row + 2 * dr, col + 2 * dc):
                        mid_piece = self.board[mid_row][mid_col]
                        if mid_piece != EMPTY and self._piece_color(mid_piece) != active:
                            jump_row = row + 2 * dr
                            jump_col = col + 2 * dc
                            if self.board[jump_row][jump_col] == EMPTY:
                                captures.extend(self._capture_sequences(self.board, row, col, active, (row, col)))
                                break
                    next_row = row + dr
                    next_col = col + dc
                    if self.in_bounds(next_row, next_col) and self.board[next_row][next_col] == EMPTY:
                        simple.append(Move((row, col), (next_row, next_col)))
        if captures:
            unique = []
            seen = set()
            for move in captures:
                key = (move.from_pos, move.to_pos, move.captured)
                if key not in seen:
                    seen.add(key)
                    unique.append(move)
            return unique
        return simple

    def _apply_capture(self, move: Move) -> "Board":
        new_board = Board(self.board, self.turn)
        start_row, start_col = move.from_pos
        end_row, end_col = move.to_pos
        piece = new_board.board[start_row][start_col]
        new_board.board[start_row][start_col] = EMPTY
        for captured_row, captured_col in move.captured:
            new_board.board[captured_row][captured_col] = EMPTY
        new_board.board[end_row][end_col] = piece
        if not self._piece_is_king(piece) and ((piece > 0 and end_row == BOARD_SIZE - 1) or (piece < 0 and end_row == 0)):
            new_board.board[end_row][end_col] = piece * 2
        new_board.turn = -self.turn
        return new_board

    def _apply_simple(self, move: Move) -> "Board":
        new_board = Board(self.board, self.turn)
        start_row, start_col = move.from_pos
        end_row, end_col = move.to_pos
        piece = new_board.board[start_row][start_col]
        new_board.board[start_row][start_col] = EMPTY
        new_board.board[end_row][end_col] = piece
        if not self._piece_is_king(piece) and ((piece > 0 and end_row == BOARD_SIZE - 1) or (piece < 0 and end_row == 0)):
            new_board.board[end_row][end_col] = piece * 2
        new_board.turn = -self.turn
        return new_board

    def apply_move(self, move: Move | Tuple[Tuple[int, int], Tuple[int, int]] | Sequence[int]) -> "Board":
        if isinstance(move, Move):
            parsed = move
        else:
            if len(move) == 2 and isinstance(move[0], tuple):
                parsed = Move(move[0], move[1])
            elif len(move) == 4:
                parsed = Move((move[0], move[1]), (move[2], move[3]))
            else:
                raise ValueError(f"Unsupported move format: {move!r}")

        if parsed.is_capture or parsed.captured:
            return self._apply_capture(parsed)
        return self._apply_simple(parsed)

    def legal_moves_for(self, color: int) -> List[Move]:
        return self.generate_moves(color)

    def winner(self) -> Optional[int]:
        black_moves = self.legal_moves_for(BLACK)
        white_moves = self.legal_moves_for(WHITE)
        if not black_moves and not white_moves:
            return 0
        if not black_moves:
            return WHITE
        if not white_moves:
            return BLACK
        return None

    def evaluate(self, perspective: int = BLACK) -> float:
        score = 0.0
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece == EMPTY:
                    continue
                sign = 1 if piece > 0 else -1
                value = 100 if abs(piece) == 1 else 180
                score += sign * value
                if piece > 0:
                    score += row * 4
                else:
                    score -= (BOARD_SIZE - 1 - row) * 4
                if abs(piece) == 1:
                    if piece > 0:
                        score += 1 if row < 6 else 0
                    else:
                        score -= 1 if row > 1 else 0
        if perspective == WHITE:
            score *= -1
        return score

    def __str__(self) -> str:
        rows = []
        for r in range(BOARD_SIZE):
            cells = []
            for c in range(BOARD_SIZE):
                piece = self.board[r][c]
                cells.append({0: '.', 1: 'b', -1: 'w', 2: 'B', -2: 'W'}[piece])
            rows.append(' '.join(cells))
        return '\n'.join(rows)


def evaluate_board(board: Board, perspective: int = BLACK) -> float:
    return board.evaluate(perspective)
