"""6x6 Rose Matrix linear-equation solver and system quantifier."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Sequence, Tuple

Matrix = Tuple[Tuple[float, ...], ...]
Vector = Tuple[float, ...]


class Matrix6x6Error(ValueError):
    """Raised when a 6x6 system is malformed or singular."""


def _matrix6(matrix: Sequence[Sequence[float]]) -> Matrix:
    if len(matrix) != 6 or any(len(row) != 6 for row in matrix):
        raise Matrix6x6Error("Rose Matrix must be exactly 6x6")
    result = tuple(tuple(float(value) for value in row) for row in matrix)
    if any(not isfinite(value) for row in result for value in row):
        raise Matrix6x6Error("matrix values must be finite")
    return result


def _vector6(vector: Sequence[float]) -> Vector:
    if len(vector) != 6:
        raise Matrix6x6Error("right-hand side must contain exactly 6 values")
    result = tuple(float(value) for value in vector)
    if any(not isfinite(value) for value in result):
        raise Matrix6x6Error("vector values must be finite")
    return result


@dataclass(frozen=True)
class SystemQuantifier:
    """Numerical quality report for a solved linear system."""

    residual_norm: float
    max_residual: float
    rank: int
    consistent: bool
    tolerance: float

    @property
    def solved(self) -> bool:
        return self.consistent and self.rank == 6

    @classmethod
    def assess(cls, matrix: Sequence[Sequence[float]], rhs: Sequence[float], solution: Sequence[float], tolerance: float = 1e-10) -> "SystemQuantifier":
        a, b, x = _matrix6(matrix), _vector6(rhs), _vector6(solution)
        if tolerance <= 0 or not isfinite(tolerance):
            raise Matrix6x6Error("tolerance must be positive and finite")
        residuals = [sum(a[i][j] * x[j] for j in range(6)) - b[i] for i in range(6)]
        max_residual = max(abs(value) for value in residuals)
        residual_norm = sum(value * value for value in residuals) ** 0.5
        rank = _rank(a, tolerance)
        return cls(residual_norm, max_residual, rank, max_residual <= tolerance, tolerance)


def _rank(matrix: Matrix, tolerance: float) -> int:
    rows = [list(row) for row in matrix]
    rank = 0
    for col in range(6):
        pivot = max(range(rank, 6), key=lambda row: abs(rows[row][col]))
        if abs(rows[pivot][col]) <= tolerance:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for row in range(rank + 1, 6):
            factor = rows[row][col] / rows[rank][col]
            for k in range(col, 6):
                rows[row][k] -= factor * rows[rank][k]
        rank += 1
    return rank


def solve_rose_matrix(matrix: Sequence[Sequence[float]], rhs: Sequence[float], tolerance: float = 1e-12) -> Vector:
    """Solve A*x=b for a nonsingular 6x6 Rose Matrix using pivoted elimination."""
    a, b = _matrix6(matrix), _vector6(rhs)
    if tolerance <= 0 or not isfinite(tolerance):
        raise Matrix6x6Error("tolerance must be positive and finite")
    aug = [list(a[i]) + [b[i]] for i in range(6)]
    for col in range(6):
        pivot = max(range(col, 6), key=lambda row: abs(aug[row][col]))
        if abs(aug[pivot][col]) <= tolerance:
            raise Matrix6x6Error("Rose Matrix is singular or ill-conditioned")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for row in range(col + 1, 6):
            factor = aug[row][col] / aug[col][col]
            for k in range(col, 7):
                aug[row][k] -= factor * aug[col][k]
    solution = [0.0] * 6
    for row in range(5, -1, -1):
        solution[row] = (aug[row][6] - sum(aug[row][j] * solution[j] for j in range(row + 1, 6))) / aug[row][row]
    return tuple(solution)


RoseMatrix6x6Solver = solve_rose_matrix
__all__ = ["Matrix6x6Error", "RoseMatrix6x6Solver", "SystemQuantifier", "solve_rose_matrix"]
