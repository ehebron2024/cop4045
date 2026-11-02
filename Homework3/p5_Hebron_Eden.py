"""Recursion exercises: recursive leaf drawings (turtle), strB, Cnk_m, make_pairs."""
import turtle
from typing import Dict, List, Optional, Sequence, Tuple, TypeVar

from testif import testif

T = TypeVar("T")
U = TypeVar("U")


# ---------------------------------------------------------------- a) leaves
def _restore(pos: Tuple[float, float], heading: float) -> None:
    """Move the turtle (without drawing) back to pos, facing heading."""
    turtle.up()
    turtle.goto(pos)
    turtle.setheading(heading)
    turtle.down()


def _lens(length: int) -> None:
    """Draw a lens-shaped leaf outline from the turtle's position along its
    heading; chord length is `length`. Postcondition: the turtle is back at
    its starting position and heading.
    """
    turtle.left(30)
    turtle.circle(-length, 60)      # first arc, bulging right of the chord
    turtle.right(120)
    turtle.circle(-length, 60)      # second arc, bulging left of the chord
    turtle.right(150)


def _blade(level: int, length: float, bend: float, side_angle: float) -> None:
    """Recursively draw a leaf blade starting at the turtle's position along
    its heading.

    Level 1 is a plain lens-shaped leaf. A higher level draws a vein for the
    first 40% of the length, then three smaller blades of level-1: one
    to the left, one to the right and one continuing to the tip.
    Parameters: bend is the total turn (degrees, clockwise) of the vein, 0
    for a straight leaf; side_angle is the angle of the side blades.
    Postcondition: turtle position and heading are restored.
    """
    start, heading = turtle.pos(), turtle.heading()
    if level <= 1:
        _lens(round(length))
        return
    steps = 4
    for _ in range(steps):                      # the (possibly curved) vein
        turtle.forward(length * 0.4 / steps)
        turtle.right(bend / steps)
    here, vein_heading = turtle.pos(), turtle.heading()
    turtle.left(side_angle)
    _blade(level - 1, length * 0.5, bend, side_angle)
    turtle.right(2 * side_angle)
    _blade(level - 1, length * 0.5, bend, side_angle)
    turtle.left(side_angle)
    _blade(level - 1, length * 0.6, bend, side_angle)
    _restore(start, heading)


def _draw_leaf(level: int, petiole: int, bend: float, x: int, y: int) -> None:
    """Common code of the two leaf functions: set up the turtle, draw the
    petiole (stem) from (x, y) pointing up, then the blade."""
    turtle.delay(0)
    turtle.tracer(0, 0)                  # draw without animation, then update
    turtle.up()
    turtle.goto(x, y)
    turtle.setheading(0)
    turtle.left(90)                      # stand vertically (default is East)
    turtle.down()
    turtle.forward(petiole)
    _blade(level, petiole * 2, bend, 40)
    turtle.update()


def draw_leaf_straight(level: int, petiole: int, x: int = 0, y: int = -250) -> None:
    """Draw a recursive straight leaf standing vertically with turtle.

    Parameters:
        level: recursion level, >= 1 (1 is a single leaf outline).
        petiole: length of the stem (petiole); the blade is twice as long.
        x, y: where the bottom of the stem is drawn.
    """
    _draw_leaf(level, petiole, 0, x, y)


def draw_leaf_curved(level: int, petiole: int, x: int = 0, y: int = -250) -> None:
    """Like draw_leaf_straight, but the veins curve to the right (extra credit)."""
    _draw_leaf(level, petiole, 40, x, y)


# ---------------------------------------------------------------- b) strB
def strB(n: int, base: int = 10) -> str:
    """Return the representation of n in the given base, recursively.

    Preconditions: n is an int >= 0; base is an int, 2 <= base <= 26.
    Digits above 9 are the letters 'A'-'Z'.
    Raises ValueError if a precondition is violated.
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if not 2 <= base <= 26:
        raise ValueError("base must be between 2 and 26")
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < base:                                   # base case: a single digit
        return digits[n]
    return strB(n // base, base) + digits[n % base]


def test_strB() -> None:
    """Unit tests for strB."""
    testif(strB(0) == "0", "strB zero")
    testif(strB(1234, base=10) == "1234", "strB base 10")
    testif(strB(1234, base=16) == "4D2", "strB base 16 uses letters")
    testif(strB(123456789, base=26) == "AA44A1", "strB base 26")
    testif(strB(100, base=2) == "1100100", "strB base 2")


# ---------------------------------------------------------------- c) Cnk_m
def Cnk_m(n: int, k: int, memo: Optional[Dict[Tuple[int, int], int]] = None) -> int:
    """Return the binomial coefficient C(n, k), recursively with memoization.

    Uses C(n,k) = C(n-1,k-1) + C(n-1,k), with C(n,0) = C(n,n) = 1. Results
    are stored in the dictionary memo, keyed by (n, k), so each is computed once.
    Preconditions: ints with 0 <= k <= n (ValueError otherwise).
    memo: optional dictionary to reuse between calls; created if omitted.
    """
    if k < 0 or k > n:
        raise ValueError("need 0 <= k <= n")
    if memo is None:
        memo = {}
    if k == 0 or k == n:
        return 1
    if (n, k) not in memo:
        memo[(n, k)] = Cnk_m(n - 1, k - 1, memo) + Cnk_m(n - 1, k, memo)
    return memo[(n, k)]


def run_Cnk(n: int, k: int) -> None:
    """Print C(n, k) computed by Cnk_m (for use from the Python console)."""
    print(f"C({n}, {k}) = {Cnk_m(n, k)}")


def test_Cnk_m() -> None:
    """Unit tests for Cnk_m."""
    testif(Cnk_m(5, 2) == 10, "Cnk_m small")
    testif(Cnk_m(10, 0) == 1 and Cnk_m(10, 10) == 1, "Cnk_m base cases")
    testif(Cnk_m(20, 10) == 184756, "Cnk_m C(20,10)")
    testif(Cnk_m(52, 5) == 2598960, "Cnk_m C(52,5)")


# ---------------------------------------------------------------- d) make_pairs
def make_pairs(seq1: Sequence[T], seq2: Sequence[U],
               acc: Optional[List[Tuple[T, U]]] = None) -> List[Tuple[T, U]]:
    """Return the list of tuples (x, y) pairing the elements of seq1 and seq2
    at the same index, stopping at the end of the shorter sequence.

    Recursive; acc is the accumulator of pairs built so far (omit it when calling).
    """
    if acc is None:
        acc = []
    if not seq1 or not seq2:                       # a sequence is exhausted
        return acc
    return make_pairs(seq1[1:], seq2[1:], acc + [(seq1[0], seq2[0])])


def test_make_pairs() -> None:
    """Unit tests for make_pairs."""
    testif(make_pairs([1, 2, 3], [4, 5, 6]) == [(1, 4), (2, 5), (3, 6)], "make_pairs equal lengths")
    testif(make_pairs([1, 2, 3], [4, 5]) == [(1, 4), (2, 5)], "make_pairs second shorter")
    testif(make_pairs([1], [4, 5, 6, 7]) == [(1, 4)], "make_pairs first shorter")
    testif(make_pairs([], [4, 5, 6]) == [], "make_pairs first empty")
    testif(make_pairs([1, 2, 3], []) == [], "make_pairs second empty")


def main() -> None:
    """Run the unit tests, then draw the straight and the curved leaf."""
    test_strB()
    test_Cnk_m()
    test_make_pairs()
    run_Cnk(30, 15)

    draw_leaf_straight(6, 120)
    input("Straight leaf drawn. Press Enter to clear and draw the curved leaf...")
    turtle.clear()
    draw_leaf_curved(6, 120)
    turtle.exitonclick()


if __name__ == "__main__":
    main()
