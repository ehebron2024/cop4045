"""
Problem 1 - Parsing Python files.

Contains:
    line_number(input_filename, output_filename)
    parse_functions(filename)

and a main() that exercises both on this very source file.
"""

import ast
import io
import os
import tokenize
from typing import Tuple


def line_number(input_filename: str, output_filename: str) -> None:
    """
    Read a text file and write a copy of it, with each line prefixed
    by its line number, to another file.

    Parameters
    ----------
    input_filename : str
        Path of the text file to read.
    output_filename : str
        Path of the file to create/overwrite with numbered lines.

    Returns
    -------
    None

    Raises
    ------
    Exception
        Re-raises whatever exception occurs (e.g. FileNotFoundError,
        PermissionError) after printing a user-friendly message.
    """
    try:
        with open(input_filename, 'r', encoding='utf-8') as fin, \
                open(output_filename, 'w', encoding='utf-8') as fout:
            for i, line in enumerate(fin, start=1):
                fout.write(f"{i}. {line}")
                if not line.endswith('\n'):
                    fout.write('\n')
    except Exception as e:
        print(f"Sorry, something went wrong while numbering the lines "
              f"of '{input_filename}': {e}")
        raise


def parse_functions(filename: str) -> Tuple[Tuple[int, str, str, str], ...]:
    """
    Parse a .py file and extract information about every top-level
    function it defines.

    Parameters
    ----------
    filename : str
        Path to the .py file to parse.

    Returns
    -------
    Tuple[Tuple[int, str, str, str], ...]
        A tuple of tuples, one per top-level function, ordered
        alphabetically by function name. Each inner tuple contains:
            0 - the line number of the function definition
            1 - the function name
            2 - the formal argument list, as a string
            3 - the function's code (signature + body) as a string,
                with all blank lines and comments removed

    Raises
    ------
    Exception
        Re-raises whatever exception occurs (e.g. FileNotFoundError,
        SyntaxError) after printing a user-friendly message.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()

        tree = ast.parse(source, filename=filename)

        # Use tokenize (not a naive '#' search) so that '#' characters
        # that appear inside strings/docstrings are never mistaken for
        # comments.
        comment_start_col = {}
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type == tokenize.COMMENT:
                line_no, col = tok.start
                comment_start_col[line_no] = col

        source_lines = source.splitlines(keepends=True)

        results = []
        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue

            name = node.name
            args = ast.unparse(node.args)
            start_line = node.lineno
            end_line = node.end_lineno

            cleaned_lines = []
            for ln in range(start_line, end_line + 1):
                text = source_lines[ln - 1]
                # Strip a trailing inline comment, if tokenize found one
                # on this physical line.
                if ln in comment_start_col:
                    text = text[:comment_start_col[ln]]
                    if not text.endswith('\n'):
                        text += '\n'
                # Drop lines that are now blank (were comment-only or
                # already blank).
                if text.strip() == '':
                    continue
                cleaned_lines.append(text)

            code = ''.join(cleaned_lines)
            results.append((start_line, name, args, code))

        results.sort(key=lambda item: item[1])
        return tuple(results)

    except Exception as e:
        print(f"Sorry, something went wrong while parsing '{filename}': {e}")
        raise


def main() -> None:
    """Test line_number and parse_functions on this problem's own file."""
    this_file = os.path.abspath(__file__)

    # a) Test line_number. Write to a differently-named file so we never
    #    overwrite this program by mistake.
    numbered_output = this_file + ".txt"
    line_number(this_file, numbered_output)
    print(f"line_number: wrote numbered copy of '{this_file}' "
          f"to '{numbered_output}'\n")

    # b) Test parse_functions and display the result.
    functions = parse_functions(this_file)
    print("parse_functions result:")
    for line_no, name, args, code in functions:
        num_lines = code.count('\n')
        print(f"  line {line_no}: {name}({args})  "
              f"[{num_lines} line(s) of code]")


if __name__ == '__main__':
    main()