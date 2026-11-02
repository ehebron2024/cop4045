"""File-system entries: Entry, File and Folder, with size and path computations."""
import unittest
from typing import List, Optional, Tuple


class Entry:
    """A named entry (file or folder) in a storage system, with an optional parent folder."""

    def __init__(self, name: str, parent: Optional["Entry"] = None) -> None:
        """Create an entry with the given name and parent (None for a root entry)."""
        self.name: str = name
        self._parent: Optional[Entry] = parent

    def parent(self) -> Optional["Entry"]:
        """Return the parent entry, or None if this is the root."""
        return self._parent

    def size(self) -> int:
        """Return the size in bytes. Must be overridden by subclasses."""
        raise NotImplementedError("subclasses must override size()")

    def absolute_path(self) -> List["Entry"]:
        """Return the absolute path as a list of Entry objects: this entry first,
        then its parent, and so on up to the root entry (recursive).
        """
        if self._parent is None:
            return [self]
        return [self] + self._parent.absolute_path()

    def __repr__(self) -> str:
        """Return a short representation: the class name and the entry's name."""
        return f"{type(self).__name__}({self.name!r})"


class File(Entry):
    """A file that uses a nonnegative number of bytes."""

    def __init__(self, name: str, bytes_used: int,
                 parent: Optional["Folder"] = None) -> None:
        """Create a file of bytes_used bytes; if parent is given, add the file to it.

        Raises ValueError if bytes_used is negative.
        """
        super().__init__(name)
        if bytes_used < 0:
            raise ValueError("bytes_used must be nonnegative")
        self.bytes_used: int = bytes_used
        if parent is not None:
            parent.add(self)

    def size(self) -> int:
        """Return the number of bytes used by this file."""
        return self.bytes_used


class Folder(Entry):
    """A folder containing files and other folders."""

    def __init__(self, name: str, parent: Optional["Folder"] = None) -> None:
        """Create an empty folder; if parent is given, add the folder to it."""
        super().__init__(name)
        self._children: List[Entry] = []
        if parent is not None:
            parent.add(self)

    def add(self, entry: Entry) -> None:
        """Add entry as a child of this folder and make this folder its parent.

        Raises ValueError if entry already has a parent, or if entry is this
        folder or one of its ancestors (which would create a cycle).
        """
        if entry.parent() is not None:
            raise ValueError(f"{entry.name} already has a parent")
        if entry in self.absolute_path():
            raise ValueError("cannot add a folder to itself or its descendants")
        entry._parent = self
        self._children.append(entry)

    def children(self) -> Tuple[Entry, ...]:
        """Return a tuple with all the direct children of this folder."""
        return tuple(self._children)

    def size(self) -> int:
        """Return the total size of all children, including those in nested folders."""
        return sum(child.size() for child in self._children)


def find_large_files(entry: Entry, minimum_size: int) -> List[File]:
    """Return all File objects of size >= minimum_size found starting from entry.

    If entry is a File, the result is [entry] when its size is at least
    minimum_size, and [] otherwise. If entry is a Folder, the result is the
    large files in all its children, searched recursively through nested folders
    (in child order); an empty folder gives [].
    """
    if isinstance(entry, File):
        return [entry] if entry.size() >= minimum_size else []
    result: List[File] = []
    for child in entry.children():          # entry is a Folder
        result.extend(find_large_files(child, minimum_size))
    return result


def build_sample() -> Folder:
    """Build the sample hierarchy used by the demo and tests (four levels deep).

    university
    ├── readme.txt (1000)
    ├── projects
    │   ├── notes.md (5000)
    │   └── cs
    │       ├── main.py (20000)
    │       ├── data.csv (900000)
    │       └── archive (empty)
    └── photos
        └── campus.jpg (250000)
    """
    root = Folder("university")
    File("readme.txt", 1000, root)
    projects = Folder("projects", root)
    File("notes.md", 5000, projects)
    cs = Folder("cs", projects)
    File("main.py", 20000, cs)
    File("data.csv", 900000, cs)
    Folder("archive", cs)
    photos = Folder("photos", root)
    File("campus.jpg", 250000, photos)
    return root


def path_string(entry: Entry) -> str:
    """Return entry.absolute_path() as a '/'-separated string from the root down."""
    return "/" + "/".join(e.name for e in reversed(entry.absolute_path()))


class TestEntries(unittest.TestCase):
    """Unit tests for sizes, absolute_path() and find_large_files()."""

    def setUp(self) -> None:
        """Build a fresh sample hierarchy for each test."""
        self.root = build_sample()
        self.projects = self.root.children()[1]
        self.cs = self.projects.children()[1]
        self.main_py = self.cs.children()[0]
        self.data_csv = self.cs.children()[1]
        self.campus = self.root.children()[2].children()[0]

    def test_size(self) -> None:
        """size() of files, empty folders and nested folders."""
        self.assertEqual(self.main_py.size(), 20000)
        self.assertEqual(self.cs.children()[2].size(), 0)
        self.assertEqual(self.root.size(), 1176000)

    def test_negative_size_rejected(self) -> None:
        """A negative file size raises ValueError."""
        with self.assertRaises(ValueError):
            File("bad", -1)

    def test_add_sets_parent(self) -> None:
        """add() sets the parent; adding twice or creating a cycle is rejected."""
        self.assertIs(self.main_py.parent(), self.cs)
        with self.assertRaises(ValueError):
            Folder("other").add(self.main_py)
        with self.assertRaises(ValueError):
            self.cs.add(self.root)

    def test_absolute_path_deep(self) -> None:
        """absolute_path() lists the entry first and the root last."""
        self.assertEqual(self.main_py.absolute_path(),
                         [self.main_py, self.cs, self.projects, self.root])

    def test_absolute_path_root(self) -> None:
        """The root's absolute path is just the root."""
        self.assertEqual(self.root.absolute_path(), [self.root])

    def test_find_large_files_folder(self) -> None:
        """find_large_files on a folder searches nested folders."""
        self.assertEqual(find_large_files(self.root, 200000),
                         [self.data_csv, self.campus])
        self.assertEqual(find_large_files(self.root, 20000),
                         [self.main_py, self.data_csv, self.campus])
        self.assertEqual(find_large_files(self.root, 10 ** 9), [])

    def test_find_large_files_file(self) -> None:
        """find_large_files on a file returns it only if it is large enough."""
        self.assertEqual(find_large_files(self.main_py, 20000), [self.main_py])
        self.assertEqual(find_large_files(self.main_py, 20001), [])

    def test_find_large_files_empty_folder(self) -> None:
        """An empty folder has no large files."""
        self.assertEqual(find_large_files(Folder("empty"), 0), [])


def main() -> None:
    """Demonstrate the classes (parts f and g), then run the unit tests (part e)."""
    root = build_sample()
    print("size() of the outer folder (files and nested folders):", root.size())
    for sub in root.children():
        print(f"  {sub.name}: {sub.size()}")

    for threshold in (200000, 10000):
        found = find_large_files(root, threshold)
        print(f"find_large_files(root, {threshold}):",
              [f"{f.name} ({f.size()})" for f in found])

    deep = find_large_files(root, 900000)[0]
    print("\nabsolute_path() of", deep.name + ":", deep.absolute_path())
    print("as a path string:", path_string(deep))
    print("absolute_path() of the root:", root.absolute_path())

    print("\nUnit tests:")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestEntries)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    main()
