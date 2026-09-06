import pytest

from dartrix_core.matrix6x6 import Matrix6x6Error, SystemQuantifier, solve_rose_matrix


def test_solves_pivoted_6x6_system():
    matrix = [[1 if i == j else 0 for j in range(6)] for i in range(6)]
    matrix[0][0], matrix[0][1] = 2, 1
    expected = (1, 2, 3, 4, 5, 6)
    rhs = [sum(matrix[i][j] * expected[j] for j in range(6)) for i in range(6)]
    solution = solve_rose_matrix(matrix, rhs)
    assert solution == pytest.approx(expected)
    report = SystemQuantifier.assess(matrix, rhs, solution)
    assert report.solved
    assert report.rank == 6
    assert report.max_residual < 1e-10


def test_rejects_non_6x6_and_singular_matrices():
    with pytest.raises(Matrix6x6Error):
        solve_rose_matrix([[1]], [1])
    with pytest.raises(Matrix6x6Error):
        solve_rose_matrix([[1] * 6 for _ in range(6)], [1] * 6)


def test_quantifier_detects_inconsistent_solution():
    identity = [[1 if i == j else 0 for j in range(6)] for i in range(6)]
    report = SystemQuantifier.assess(identity, [0] * 6, [1, 0, 0, 0, 0, 0])
    assert not report.solved
    assert report.consistent is False
