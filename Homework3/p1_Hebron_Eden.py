from __future__ import annotations

from numbers import Number
from typing import Any, Iterable, Union

from testif import testif


class NVector:
    """An N-dimensional vector of real numbers, stored in a Python list."""

    def __init__(self, *args: Any) -> None:
        """Create a vector.

        With exactly one argument, it must be a sequence (or other iterable)
        of numbers; its elements are copied into a new list.
        With zero or two or more arguments, the arguments are the elements.

        Raises TypeError if a single argument is not iterable.
        """
        if len(args) == 1:
            self._elements: list = list(args[0])
        else:
            self._elements = list(args)

    def __len__(self) -> int:
        """Return the number of elements (the dimension) of the vector."""
        return len(self._elements)

    def __getitem__(self, index: int) -> float:
        """Return the element at index; negative indexes count from the end.

        Raises IndexError if index is out of range, TypeError if not an int.
        """
        return self._elements[index]

    def __setitem__(self, index: int, value: float) -> None:
        """Set the element at index to value; negative indexes are allowed.

        Postcondition: self[index] == value.
        Raises IndexError if index is out of range, TypeError if not an int.
        """
        self._elements[index] = value

    def __str__(self) -> str:
        """Return a string such as '[3, 0, 1, -1]'."""
        return str(self._elements)

    def __repr__(self) -> str:
        """Return an unambiguous representation such as 'NVector([3, 0])'."""
        return "NVector(" + str(self._elements) + ")"

    def __eq__(self, other: object) -> bool:
        """Return True iff other is an NVector with equal elements in order."""
        if not isinstance(other, NVector):
            return False
        return self._elements == other._elements

    def __ne__(self, other: object) -> bool:
        """Return the negation of __eq__."""
        return not self.__eq__(other)

    def __add__(self, other: Union[NVector, float]) -> NVector:
        """Return self + other as a new NVector.

        If other is an NVector, add element-wise (dimensions must match,
        otherwise ValueError is raised). If other is a number, add it to
        every element. Other types give NotImplemented (-> TypeError).
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("vectors must have the same dimension")
            return NVector([a + b for a, b in zip(self._elements, other._elements)])
        if isinstance(other, Number):
            return NVector([a + other for a in self._elements])
        return NotImplemented

    def __radd__(self, other: float) -> NVector:
        """Reflected addition: number + NVector. Same result as self + other."""
        return self.__add__(other)

    def __mul__(self, other: Union[NVector, float]) -> float:
        """Return the scalar product of self with other (a number).

        If other is an NVector, the result is the sum of Ai*Bi (dimensions
        must match, otherwise ValueError is raised). If other is a number,
        the result is the sum of Ai*other.
        Other types give NotImplemented (-> TypeError).
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("vectors must have the same dimension")
            return sum(a * b for a, b in zip(self._elements, other._elements))
        if isinstance(other, Number):
            return sum(a * other for a in self._elements)
        return NotImplemented

    def __rmul__(self, other: float) -> float:
        """Reflected multiplication: number * NVector. Same as self * other."""
        return self.__mul__(other)

    @classmethod
    def zeros(cls, n: int) -> NVector:
        """Return a new n-dimensional NVector with all elements 0.

        Precondition: n is a non-negative int (ValueError if negative).
        """
        if n < 0:
            raise ValueError("dimension must be non-negative")
        return cls([0] * n)


def raises(exc: type, f) -> bool:
    """Return True iff calling f() raises exc."""
    try:
        f()
    except exc:
        return True
    except Exception:
        return False
    return False


def main() -> None:
    """Test the NVector class using testif."""
    # a) constructor with a sequence
    lst = [3, 0, 1, -1]
    v = NVector(lst)
    testif(len(v) == 4 and v[0] == 3, "constructor from list", "ok", "failed")
    lst[0] = 99
    testif(v[0] == 3, "constructor copies list", "no sharing", "list shared")
    testif(NVector((3, 0, 1, -1)) == NVector([3, 0, 1, -1]), "constructor from tuple")
    testif(raises(TypeError, lambda: NVector(5)), "scalar single argument raises TypeError")

    # b) constructor with several arguments
    v = NVector(3, 0, 1, -1)
    testif(len(v) == 4 and v[3] == -1, "constructor from varargs")

    # c) __len__
    testif(v.__len__() == 4 and len(NVector.zeros(0)) == 0, "len works")

    # d) __getitem__
    testif(v[1] == 0, "getitem positive index")
    testif(v[-2] == 1, "getitem negative index")
    testif(raises(IndexError, lambda: v[4]), "getitem out of range raises IndexError")

    # e) __setitem__
    v[3] = 10
    testif(v[3] == 10, "setitem works", "setitem failed")
    v[-4] = 7
    testif(v[0] == 7, "setitem negative index")
    def bad_set() -> None:
        v[10] = 1
    testif(raises(IndexError, bad_set), "setitem out of range raises IndexError")

    # f) __str__
    testif(str(NVector(3, 0, 1, -1)) == "[3, 0, 1, -1]", "str works")

    # g) __eq__ and __ne__
    a, b = NVector(1, 2, 3), NVector([1, 2, 3])
    testif(a == b, "eq equal vectors")
    testif(not (a != b), "ne equal vectors")
    testif(a != NVector(1, 2, 4), "ne different elements")
    testif(a != NVector(1, 2), "ne different lengths")
    testif(a != [1, 2, 3] and not (a == [1, 2, 3]), "comparison with non-NVector")

    # h) __add__ and __radd__
    x = NVector([3, 0, 1, -1])
    testif(x + NVector([1, 2, 3, 4]) == NVector([4, 2, 4, 3]), "add vectors")
    testif(x + 10 == NVector([13, 10, 11, 9]), "add number")
    testif(10 + x == NVector([13, 10, 11, 9]), "radd number")
    testif(x == NVector([3, 0, 1, -1]), "add does not modify operands")
    testif(raises(ValueError, lambda: x + NVector(1, 2)), "add mismatched dimensions raises ValueError")
    testif(raises(TypeError, lambda: x + "a"), "add string raises TypeError")

    # i) __mul__ and __rmul__
    testif(x * NVector([1, 2, 3, 4]) == 2, "mul vectors (dot product)")
    testif(x * 2 == 6, "mul number")
    testif(2 * x == 6, "rmul number")
    testif(raises(ValueError, lambda: x * NVector(1, 2)), "mul mismatched dimensions raises ValueError")
    testif(raises(TypeError, lambda: x * "a"), "mul string raises TypeError")

    # j) zeros
    z = NVector.zeros(3)
    testif(z == NVector(0, 0, 0) and len(z) == 3, "zeros works")
    testif(raises(ValueError, lambda: NVector.zeros(-1)), "zeros negative raises ValueError")


if __name__ == "__main__":
    main()
