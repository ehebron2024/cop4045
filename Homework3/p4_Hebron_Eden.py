"""A tiny non-interactive text editor: ed_read, ed_find, ed_replace, ed_append.

Files are utf-8 encoded and read entirely into memory. Files are opened with
newline="" so no newline translation happens and positions are always
character indexes into the file's exact text. File I/O errors
(FileNotFoundError, IOError, ...) are never caught here: they go to the caller.
"""
import os
import tempfile
from typing import List

from testif import testif

ENCODING = "utf-8"


def _load(filename: str) -> str:
    """Return the entire content of filename as a string (I/O errors propagate)."""
    with open(filename, "r", encoding=ENCODING, newline="") as f:
        return f.read()


def _save(filename: str, text: str) -> None:
    """Overwrite filename with text (I/O errors propagate)."""
    with open(filename, "w", encoding=ENCODING, newline="") as f:
        f.write(text)


def _positions(text: str, search_str: str) -> List[int]:
    """Return the start indexes of the non-overlapping occurrences of
    search_str in text, scanning left to right.

    Precondition: search_str is not empty.
    """
    result: List[int] = []
    i = text.find(search_str)
    while i != -1:
        result.append(i)
        i = text.find(search_str, i + len(search_str))
    return result


def ed_read(filename: str, from_pos: int = 0, to: int = -1) -> str:
    """Return the content of the file in the half-open range [from_pos, to).

    (The parameter is named from_pos because "from" is a Python keyword.)

    Parameters:
        filename: name of an existing utf-8 text file.
        from_pos: first index to return; 0 <= from_pos <= to.
        to: index just past the last one returned; -1 means the end of the file.
    Returns: the selected substring. The file is not modified.
    Raises:
        IndexError: if to exceeds the file length, or from_pos is negative or
            past the end of the file.
        ValueError: if from_pos > to.
        FileNotFoundError, IOError: passed to the caller.
    """
    text = _load(filename)
    if to == -1:
        to = len(text)
    if to > len(text):
        raise IndexError(f"to ({to}) exceeds file length ({len(text)})")
    if from_pos < 0 or from_pos > len(text):
        raise IndexError(f"from ({from_pos}) is outside the file (length {len(text)})")
    if from_pos > to:
        raise ValueError(f"from ({from_pos}) is greater than to ({to})")
    return text[from_pos:to]


def ed_find(filename: str, search_str: str) -> List[int]:
    """Return the index positions where search_str occurs in the file.

    Occurrences are non-overlapping, scanned left to right (so finding "aa" in
    "aaa" gives [0]), which matches what ed_replace counts as occurrences.

    Parameters:
        filename: name of an existing utf-8 text file.
        search_str: the string to look for; must not be empty.
    Returns: ascending list of start indexes; [] if not found. The file is
        not modified.
    Raises:
        ValueError: if search_str is empty.
        FileNotFoundError, IOError: passed to the caller.
    """
    if search_str == "":
        raise ValueError("search_str must not be empty")
    return _positions(_load(filename), search_str)


def ed_replace(filename: str, search_str: str, replace_with: str,
               occurrence: int = -1) -> int:
    """Replace occurrences of search_str in the file with replace_with.

    Parameters:
        filename: name of an existing utf-8 text file.
        search_str: the string to replace; must not be empty.
        replace_with: the replacement string (may be empty).
        occurrence: -1 replaces all occurrences; k >= 0 replaces only the
            occurrence with index k (0 is the first). If the file has no
            occurrence k, nothing is replaced.
    Returns: the number of replacements made. The file is rewritten only if
        that number is positive; it is unchanged on any error.
    Raises:
        ValueError: if search_str is empty or occurrence < -1.
        FileNotFoundError, IOError: passed to the caller.
    """
    if search_str == "":
        raise ValueError("search_str must not be empty")
    if occurrence < -1:
        raise ValueError("occurrence must be -1 or a non-negative index")
    text = _load(filename)
    positions = _positions(text, search_str)
    if occurrence != -1:
        positions = positions[occurrence:occurrence + 1]   # [] if out of range
    if not positions:
        return 0
    pieces: List[str] = []
    last = 0
    for p in positions:
        pieces.append(text[last:p])
        pieces.append(replace_with)
        last = p + len(search_str)
    pieces.append(text[last:])
    _save(filename, "".join(pieces))
    return len(positions)


def ed_append(filename: str, string: str) -> int:
    """Append string to the end of the file, creating the file if needed.

    Parameters:
        filename: name of the file (need not exist).
        string: the text to append.
    Returns: the number of characters written (len(string)).
    Raises:
        TypeError: if string is not a str (the file is not touched).
        IOError: passed to the caller.
    """
    if not isinstance(string, str):
        raise TypeError("string must be a str")
    with open(filename, "a", encoding=ENCODING, newline="") as f:
        return f.write(string)


def _reset(filename: str, content: str) -> None:
    """Test helper: set the file content to content."""
    _save(filename, content)


def test_ed_find(fn: str) -> None:
    """Unit tests for ed_find, using the file named fn (its content is overwritten)."""
    _reset(fn, "01234567890123456789")
    testif(ed_find(fn, "345") == [3, 13], "ed_find two matches")
    testif(ed_find(fn, "356") == [], "ed_find no match")
    testif(ed_find(fn, "0") == [0, 10], "ed_find match at start")
    testif(ed_find(fn, "9") == [9, 19], "ed_find match at end")
    testif(ed_find(fn, "01234567890123456789") == [0], "ed_find whole file")
    _reset(fn, "aaaa")
    testif(ed_find(fn, "aa") == [0, 2], "ed_find non-overlapping matches")
    _reset(fn, "")
    testif(ed_find(fn, "a") == [], "ed_find empty file")
    try:
        ed_find(fn, "")
        testif(False, "ed_find empty search_str raises ValueError")
    except ValueError:
        testif(True, "ed_find empty search_str raises ValueError")
    try:
        ed_find("no_such_file_xyz.txt", "a")
        testif(False, "ed_find missing file raises FileNotFoundError")
    except FileNotFoundError:
        testif(True, "ed_find missing file raises FileNotFoundError")


def test_ed_replace(fn: str) -> None:
    """Unit tests for ed_replace, using the file named fn (its content is overwritten)."""
    original = "01234567890123456789"
    _reset(fn, original)
    n = ed_replace(fn, "345", "ABCDE", 1)
    testif(n == 1 and _load(fn) == "0123456789012ABCDE6789", "ed_replace second occurrence")
    _reset(fn, original)
    n = ed_replace(fn, "345", "ABCDE")
    testif(n == 2 and _load(fn) == "012ABCDE6789012ABCDE6789", "ed_replace all occurrences")
    _reset(fn, original)
    n = ed_replace(fn, "345", "X", 0)
    testif(n == 1 and _load(fn) == "012X67890123456789", "ed_replace first occurrence")
    _reset(fn, original)
    n = ed_replace(fn, "345", "X", 2)
    testif(n == 0 and _load(fn) == original, "ed_replace occurrence out of range changes nothing")
    n = ed_replace(fn, "xyz", "X")
    testif(n == 0 and _load(fn) == original, "ed_replace string not found changes nothing")
    n = ed_replace(fn, "345", "")
    testif(n == 2 and _load(fn) == "01267890126789", "ed_replace with empty string deletes")
    _reset(fn, "aaaa")
    n = ed_replace(fn, "aa", "b")
    testif(n == 2 and _load(fn) == "bb", "ed_replace non-overlapping matches")
    _reset(fn, "abc")
    try:
        ed_replace(fn, "", "x")
        testif(False, "ed_replace empty search_str raises ValueError")
    except ValueError:
        testif(_load(fn) == "abc", "ed_replace empty search_str raises ValueError, file unchanged")
    try:
        ed_replace(fn, "a", "x", -2)
        testif(False, "ed_replace occurrence < -1 raises ValueError")
    except ValueError:
        testif(_load(fn) == "abc", "ed_replace occurrence < -1 raises ValueError, file unchanged")
    try:
        ed_replace("no_such_file_xyz.txt", "a", "x")
        testif(False, "ed_replace missing file raises FileNotFoundError")
    except FileNotFoundError:
        testif(True, "ed_replace missing file raises FileNotFoundError")


def main() -> None:
    """Show how to use all the ed_... functions, then run the unit tests."""
    with tempfile.TemporaryDirectory() as folder:
        fn = os.path.join(folder, "file1.txt")

        print("ed_append returned", ed_append(fn, "0123456789"))  # creates the file
        print("ed_append returned", ed_append(fn, "0123456789"))
        print("content:", ed_read(fn))
        print("ed_read(fn, 3, 9):", ed_read(fn, 3, 9))
        print("ed_read(fn, 3):", ed_read(fn, 3))
        try:
            ed_read(fn, 3, 100)
        except IndexError as e:
            print("ed_read(fn, 3, 100) raised IndexError:", e)

        print("ed_find(fn, '345'):", ed_find(fn, "345"))
        print("ed_find(fn, '356'):", ed_find(fn, "356"))

        print("ed_replace(fn, '345', 'ABCDE', 1) replaced",
              ed_replace(fn, "345", "ABCDE", 1))
        print("content:", ed_read(fn))

        _reset(fn, "01234567890123456789")
        print("ed_replace(fn, '345', 'ABCDE') replaced",
              ed_replace(fn, "345", "ABCDE"))
        print("content:", ed_read(fn))

        try:
            ed_read(os.path.join(folder, "missing.txt"))
        except FileNotFoundError as e:
            print("missing file raised FileNotFoundError:", e)

        print("\nUnit tests:")
        test_ed_find(fn)
        test_ed_replace(fn)


if __name__ == "__main__":
    main()
