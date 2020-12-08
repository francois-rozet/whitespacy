#!usr/bin/env python

import os
import re

OPS = ['=', '<', '>', '+', '-', '*', '/', '^', '&', '|', '!', '(', ')', '{', '}', '[', ']', ',', ';', '.', '#', '"']

def escapeOp(op: str) -> str:
    return f'\\{op}' if op in r'^$+*.|()[]' else op


def removeComments(code: str) -> str:
    cleaned = ''
    in_comment = False

    i = 0
    while i < len(code):
        if in_comment:
            if code[i:i+2] == '*/':
                in_comment = False
                i += 1
            i += 1
        else:
            if code[i:i+2] == '/*':
                in_comment = True
                i += 2
                continue
            elif code[i:i+2] == '//':
                i = code.find('\n', i + 2)

                if i == -1:
                    break
            elif code[i] == '"':
                j = i
                while True:
                    j = code.find('"', j + 1)

                    if j == -1:
                        raise ValueError('Unterminated string')

                    if code[j-1] != '\\':
                        break

                cleaned += code[i:j]
                i = j

            cleaned += code[i]
            i += 1

    return cleaned


def removeLF(code: str) -> str:
    # Remove trailing spaces
    code = re.sub(r'[ \t]+$', r'', code, flags=re.MULTILINE)

    # Remove escapes
    code = re.sub(r'\\\n', r'', code)

    # Remove indentation
    code = re.sub(r'^[ \t]+', r'', code, flags=re.MULTILINE)

    # Remove unnecessary line feeds
    code = re.sub(r'\n+', r'\n', code)

    ## Remove all line feeds, except preprocessor directives
    code = re.sub(
        r'(.*)\n(?!#)',
        lambda x: x.group(1) + ('\n' if x.group(1)[0] == '#' else ''),
        code
    )

    return code


def removeST(code: str) -> str:
    # Replace tabs by spaces
    code = code.replace('\t', ' ')

    # Remove unnecessary spaces
    code = re.sub(r'[ ]+', r' ', code)

    ## Remove spaces around operators
    for op in OPS:
        code = re.sub(r'[ ]?' + escapeOp(op) + r'[ ]?', op, code)

    return code


def restore(code: str, strings: list) -> str:
    # Replace from last to first
    for i, string in enumerate(reversed(strings)):
        j = len(strings) - i - 1
        code = code.replace(f'${j}', string, 1)

    return code


def minifyC(code: str, apart: bool = False) -> str: # or tuple[str, list[str]]
    # Remove comments
    code = removeComments(code)

    # Remove linefeeds
    code = removeLF(code)

    # Export strings
    strings = []

    def export(m: re.Match) -> str:
        string = m.group(1)
        string = string.replace(' ', r'\x20')
        string = string.replace('\t', r'\t')

        strings.append(string)

        return '${}'.format(len(strings) - 1)

    code = re.sub(r'(\"(\\.|[^\"])*\")', export, code)

    # Remove spaces and tabs
    code = removeST(code)

    if apart:
        return code, strings
    else:
        return restore(code, strings)


def main(input_file: str, output_file: str = None, show: bool = False) -> str:
    with open(input_file) as f:
        code = f.read()

    code = minifyC(code)

    if show:
        print(code)

    if output_file is not None:
        with open(output_file, 'w') as f:
            f.write(code)

    return code

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Minify C file')

    parser.add_argument('input', help='input file to minify')
    parser.add_argument('-o', '--output', default=None, help='output file')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='print minified version on std')

    args = parser.parse_args()

    main(
        args.input,
        args.output,
        args.verbose
    )
