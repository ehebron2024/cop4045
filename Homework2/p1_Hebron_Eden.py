# Part a: Write a function called line_number...
def line_number(file_read: str, file_write: str) -> None:
    """ Defining a function that takes two file names, reads the first file, and writes the line numbers of the first file into the second one. No return value. """

    try:
        with open(file_read, 'r') as f_read, \
                open(file_write, 'w') as f_write:
            for number, line in enumerate(f_read, start=1):
                f_write.write(f'{number}. {line}')

    except OSError as error: #error handling if file is not found or cannot be opened
        print(f"Files not found: {error}")
        raise
# Part b: Write a function called parse_functions...
def parse_functions(file_read: str) -> tuple:
    """Reading Python file and returns the information as a tuple"""

    functions = []

    try:
        with open(file_read, 'r') as f_read:
            lines = f_read.readlines()

        number = 0

        while number < len(lines):
            line = lines[number]

            if line.strip().startswith('def '):
                function_line = line.strip()

                start = function_line.find('def ') + 4
                end = function_line.find('(', start)
                function_name = function_line[start:end].strip()

                arg_start = function_line.find('(') + 1
                arg_end = function_line.find(')', arg_start)
                arguments = function_line[arg_start:arg_end].strip()

                function_code = function_line + '\n'

                body_indent = None
                next_line = number + 1

                while next_line < len(lines):
                    current_line = lines[next_line]

                    if current_line.strip() == '':
                        next_line += 1
                        continue

                    indent = len(current_line) - len(current_line.lstrip())

                    if body_indent is None:
                        body_indent = indent

                    if indent < body_indent:
                        break

                    if current_line.strip().startswith(chr(35)):
                        next_line += 1
                        continue

                    if chr(35) in current_line:
                        current_line = current_line.split(chr(35))[0].rstrip() + '\n'

                    if current_line.strip():
                        function_code += current_line

                    next_line += 1

                functions.append(
                    (
                        number + 1,
                        function_name,
                        arguments,
                        function_code
                    )
                )

                number = next_line
            else:
                number += 1

        #   Sorting alphabetically
        functions.sort(key=lambda item: item[1])

        return tuple(functions)

    #   user-friendly message and raise the error again
    except OSError as error:
        print(f"Error reading the file: {error}")
        raise

    #   main function
def main():
    ''' Testing the functions '''

    line_number('p1_Hebron_Eden.py',
                'p1_Hebron_Eden.py.txt')

    functions = parse_functions('p1_Hebron_Eden.py')

    print(functions)


if __name__ == '__main__':
    main()

