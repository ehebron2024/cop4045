import ast
import tokenize


def line_number(in_file_name: str, out_file_name: str) -> None:
    """Read a text file and write its lines, each prefixed with its line number, to another file.

    Parameters:
        in_file_name (str): name of the text file to read.
        out_file_name (str): name of the text file to write the numbered lines to.

    Returns:
        None
    """
    try:
        with open(in_file_name, 'r') as in_file:
            lines = in_file.readlines()

        with open(out_file_name, 'w') as out_file:
            for i, line in enumerate(lines, start=1):
                out_file.write(f'{i}. {line}')
    except Exception as e:
        print(f'Error: could not process file(s) "{in_file_name}" and "{out_file_name}": {e}')
        raise


def parse_functions(file_name: str) -> tuple:
    """Parse a Python source file and describe every top-level function it defines.

    Parameters:
        file_name (str): name of the .py file to parse.

    Returns:
        tuple: a tuple of tuples, one per top-level function, ordered alphabetically
            by function name. Each inner tuple holds:
                0 - the line number of the function definition,
                1 - the function name,
                2 - the formal argument list as a string,
                3 - the function's code (signature and body) as a string, with all
                    empty lines and comments removed.
    """
    try:
        with open(file_name, 'r') as f:
            source = f.read()
        lines = source.splitlines()

        comment_cols = {}
        with open(file_name, 'rb') as f:
            for tok in tokenize.tokenize(f.readline):
                if tok.type == tokenize.COMMENT:
                    comment_cols[tok.start[0]] = tok.start[1]

        tree = ast.parse(source, filename=file_name)

        functions = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                start = node.lineno
                end = node.end_lineno
                args = ', '.join(arg.arg for arg in node.args.args)

                code_lines = []
                for ln in range(start, end + 1):
                    line_text = lines[ln - 1]
                    if ln in comment_cols:
                        line_text = line_text[:comment_cols[ln]]
                    if line_text.strip() == '':
                        continue
                    code_lines.append(line_text.rstrip())
                code = '\n'.join(code_lines) + '\n'

                functions.append((start, node.name, args, code))

        functions.sort(key=lambda item: item[1])
        return tuple(functions)
    except Exception as e:
        print(f'Error: could not parse file "{file_name}": {e}')
        raise


def main() -> None:
    """Test line_number and parse_functions on this program's own source file."""
    line_number('p1_Hebron_Eden.py', 'p1_Hebron_Eden_output.txt')

    functions = parse_functions('p1_Hebron_Eden.py')
    for line_no, name, args, code in functions:
        print(f'Line {line_no}: {name}({args})')
        print(code)


if __name__ == '__main__':
    main()
