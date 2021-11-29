"""Pure python implementation of some basic modular algebra"""
from itertools import product


class ModMatrix:
    """Square matrix for modular arithmetics"""

    def __init__(self, size, initial=0, diagonal=None, modulo=2):
        """
        Creates a square matrix of order _size_ filled with the _initial_
        value, sets the _diagonal_ value if specified and uses the
        _modulo_ parameter in all arithmetic operations.
        """

        if size <= 0:
            raise ValueError(f"Expected stricly positive integer, not {size=}")

        self.size = size
        self.mod = modulo
        self.data = list()

        value = initial % modulo
        for _ in range(size):
            self.data.append([value] * size)

        if diagonal:
            value = diagonal % modulo
            for i in range(size):
                self.data[i][i] = value

    def __len__(self):
        """The order of the square matrix"""
        return self.size

    def __reversed__(self):
        raise TypeError("Cannot reverse matrix data. Are you looking for transposed?")

    def __getitem__(self, postion):
        """Access matrix item at (row, col) position"""
        row, col = postion
        return self.data[row][col]

    def __setitem__(self, position, value):
        """Set matrix value at (row, col) position"""
        row, col = position
        self.data[row][col] = value % self.mod

    def __iter__(self):
        """All (position, value) tuples iterator"""
        for row in range(self.size):
            for col in range(self.size):
                yield (row, col), self.data[row][col]

    def positions(self):
        """All (row, col) positions iterator"""
        yield from (product(range(self.size), range(self.size)))

    def values(self):
        """All data values iterator"""
        for row in range(self.size):
            yield from self.data[row]

    def _validate_operand(self, other):
        if self.size != other.size:
            raise ValueError(
                f"Matrix operation requires same size, {self.size} vs {other.size}"
            )
        if self.mod != other.mod:
            raise TypeError(
                f"Operands have different modulo setting, {self.mod} vs {other.mod}"
            )

    def __eq__(self, other):
        """Compares matrix values for equality"""
        return all(left == right for left, right in zip(self.values(), other.values()))

    def __add__(self, other):
        """Matrix addition"""
        self._validate_operand(other)
        result = self.__class__(self.size, self.mod)

        for pos in self.positions():
            result[pos] = (self[pos] + other[pos]) % self.mod

        return result

    def __sub__(self, other):
        """Matrix substraction"""
        self._validate_operand(other)

        result = self.__class__(self.size, self.mod)
        for pos in self.positions():
            result[pos] = (self[pos] - other[pos]) % self.mod

        return result

    def __mul__(self, other):
        """Matrix multiplication"""
        self._validate_operand(other)

        result = self.__class__(self.size, modulo=self.mod)
        for row in range(self.size):
            for col in range(self.size):
                result[row, col] = sum(
                    self[row, i] * other[i, col] for i in range(self.size)
                )

        return result

    def transposed(self):
        """Transposed matrix iterator"""
        for row in range(self.size):
            for col in range(self.size):
                yield (row, col), self.data[col][row]

    def transpose(self):
        """Returns a transposed copy of the matrix"""
        other = self.__class__(self.size, modulo=self.mod)

        for row in range(self.size):
            for col in range(self.size):
                other.data[row][col] = self.data[col][row]

        return other

    def diagonal(self):
        """Diagonal values iterator"""
        yield from (self.data[i][i] for i in range(self.size))

    def print(self, label=None):
        """Prints matrix to console"""
        if label:
            print(f"{label} =")
        for row in self.data:
            print("   ", row)


def determinant(matrix, mod=2):
    # TODO: move to matrix class
    size = len(matrix)
    assert size == len(matrix[0]), "Expected a square matrix"

    if size == 1:
        return matrix[0][0] % mod

    for row in range(size):
        for col in range(size):
            matrix[row][col] %= mod

    if size == 2:
        return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % mod

    raise NotImplemented(f"Higher order matrix ({size})")


if __name__ == "__main__":
    print("This is a pure module, so it must be imported.")
