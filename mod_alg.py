"""Pure python implementation of some basic modular algebra"""


class ModMatrix:
    """Square matrix for modular arithmetics"""

    def __init__(self, size, fill_with=0, diagonal=None, mod=2):
        """
        Creates a `size` order matrix filled with an initial value and sets diagonal
        value if specified.
        """

        if size <= 0:
            raise ValueError(f"Expected stricly positive integer, not {size=}")

        self.size = size
        self.mod = mod
        self.data = list()

        value = fill_with % mod
        for _ in range(size):
            self.data.append([value] * size)

        if diagonal:
            value = diagonal % mod
            for i in range(size):
                self.data[i][i] = value

    def __len__(self):
        """Should this return the size squared?"""
        return self.size

    def __reversed__(self):
        raise TypeError("A matrix cannot be reversed")

    def __getitem__(self, key):
        row, col = key
        return self.data[row][col]

    def __setitem__(self, key, value):
        row, col = key
        self.data[row][col] = value % self.mod

    def __iter__(self):
        for row in range(self.size):
            for col in range(self.size):
                yield (row, col), self.data[row][col]

    def positions(self):
        for row in range(self.size):
            for col in range(self.size):
                yield (row, col)

    def values(self):
        for row in range(self.size):
            yield from self.data[row]

    def _validate_operand(self, other):
        if self.size != other.size:
            raise ValueError(f"Expected equal sized operands, {self.size} vs {other.size}")
        if self.mod != other.mod:
            raise TypeError(f"Operands have different modulo setting, {self.mod} vs {other.mod}")

    def __eq__(self, other):
        return all(left == right for left, right in zip(self.values(), other.values()))

    def __add__(self, other):
        self._validate_operand(other)
        result = self.__class__(self.size, self.mod)

        for pos in self.positions():
            result[pos] = (self[pos] + other[pos]) % self.mod

        return result

    def __sub__(self, other):
        self._validate_operand(other)

        result = self.__class__(self.size, self.mod)
        for pos in self.positions():
            result[pos] = (self[pos] - other[pos]) % self.mod

        return result

    def __mul__(self, other):
        """dot product"""
        self._validate_operand(other)

        result = self.__class__(self.size, mod=self.mod)
        for row in range(self.size):
            for col in range(self.size):
                total = 0
                for i in range(self.size):
                    total += self[row, i] * other[i, col]
                result[row, col] = total

        return result

    def transposed(self):
        """returns a transposed iterator"""
        for row in range(self.size):
            for col in range(self.size):
                yield (row, col), self.data[col][row]

    def transpose(self):
        """returns a transposed copy"""
        other = self.__class__(self.size, mod=self.mod)
        for row in range(self.size):
            for col in range(self.size):
                other.data[row][col] = self.data[col][row]
        return other

    def diagonal(self):
        yield from (self.data[i][i] for i in range(self.size))

    def print(self, label=None):
        if label:
            print(f" ..: {label}")
        for row in self.data:
            print("    ", row)


def determinant(matrix, mod=2):
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
