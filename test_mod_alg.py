import pytest
from mod_alg import ModMatrix


def test_empty_matrix_raises_error():
    with pytest.raises(ValueError):
        a = ModMatrix(0)


def test_zero_filled_matrix():
    one = ModMatrix(1)
    two = ModMatrix(2)
    three = ModMatrix(3)

    for pos, value in one:
        assert value == 0, f"Element at {pos} is not zero, {value=}"

    for pos, value in two:
        assert value == 0, f"Element at {pos} is not zero, {value=}"

    for pos, value in three:
        assert value == 0, f"Element at {pos} is not zero, {value=}"


def test_diagonal_filled_matrix():
    one = ModMatrix(1, diagonal=1)
    two = ModMatrix(2, diagonal=3)
    three = ModMatrix(3, diagonal=5)

    for (row, col), value in one:
        expected = 1 if row == col else 0
        assert value == expected, f"Element at {row, col} is not {expected}, {value=}"

    for (row, col), value in two:
        expected = 1 if row == col else 0
        assert value == expected, f"Element at {row, col} is not {expected}, {value=}"

    for (row, col), value in three:
        expected = 1 if row == col else 0
        assert value == expected, f"Element at {row, col} is not {expected}, {value=}"

    for value in three.diagonal():
        assert value == 1


def test_transpositions():
    alt_cols = ModMatrix(4)

    for row, col in alt_cols.positions():
        alt_cols[row, col] = 1 - col
    alt_cols.print("Alternating cols")

    alt_rows = alt_cols.transpose()
    alt_rows.print("Alternating rows")

    for (row, col), value in alt_rows:
        expected = (1 - row) % alt_rows.mod
        assert value == expected, f"transposed value failed at {row, col}"


def test_mod_addition():
    a = ModMatrix(4, initial=1)
    b = ModMatrix(4, diagonal=1)

    a.print("A")
    b.print("B")

    res = a + b
    res.print("A+B")

    for pos, value in res:
        expected = (a[pos] + b[pos]) % a.mod
        assert value == expected, f"Addition failed at {pos=}"


def test_mod_substraction():
    a = ModMatrix(4, initial=1)
    b = ModMatrix(4, diagonal=1)

    a.print("A")
    b.print("B")

    res = a - b
    res.print("A-B")

    for pos, value in res:
        expected = (a[pos] - b[pos]) % a.mod
        assert value == expected, f"Substraction failed at {pos=}"


def test_mod_multiply():
    a = ModMatrix(2, modulo=100)
    b = ModMatrix(2, modulo=100)
    expected = ModMatrix(2, modulo=100)

    a.data = [
        [4, 2],
        [0, 3],
    ]
    b.data = [
        [4, 0],
        [1, 4],
    ]
    expected.data = [
        [18, 8],
        [3, 12],
    ]

    res = a * b

    a.print("A")
    b.print("B")
    res.print("A * B")

    assert res == expected
