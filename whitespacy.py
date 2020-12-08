#!usr/bin/env python

import os
import random
import itertools

from minic import minifyC, restore

OPS = ['=', '+', '-', '*', '/', '^', '&', '|', '!', '(', ')', '{', '}', '[', ']', ',', ';', '#']


def sub_indices(string: str, sub: str): # -> list[int]
    stack = []

    i = string.find(sub)
    while i != -1:
        stack.append(i)
        i = string.find(sub, i + len(sub))

    return stack


def indices_split(string: str, indices: list): # -> list[str]
    splits = []

    for i, j in zip([0] + indices, indices + [len(string)]):
        splits.append(string[i:j])

    return splits


def random_chunk(string: str, n: int, lower: int = 0): # -> list[str]
    widths = []
    remain = len(string)

    for i in range(n):
        widths.append(random.randint(lower, remain - (n - i - 1) * lower))
        remain -= widths[-1]

    random.shuffle(widths)

    indices = list(itertools.accumulate(widths))[:-1]
    chunks = indices_split(string, indices)

    return chunks


def divide(code: str): # -> list[str]
    atoms = ['']

    for ch in code:
        if ch in OPS:
            atoms.append(ch)
            atoms.append('')
        else:
            atoms[-1] += ch

    if atoms[0] == '':
        atoms = atoms[1:]

    if atoms[-1] == '':
        atoms.pop()

    return atoms


def merge(code: str, white: str) -> str:
    bits = divide(code)
    chunks = random_chunk(white, len(bits))

    return ''.join(a + b for a, b in zip(chunks, bits))


def whitifyC(code: str, white: str) -> str:
    code, strings = minifyC(code, apart=True)
    whitified = ''

    i = 0

    lines = code.split('\n')

    for nl, line in enumerate(lines):
        # Bits of code without spacing
        bits = line.split(' ')

        ## Min number of spaces
        n = len(bits) - 1

        # Merge
        j = i
        while True:
            if j == len(white):
                raise ValueError('Not enough linefeeds or spaces')

            if nl < len(lines) - 1:
                j = white.find('\n', j)

                if j == -1:
                    j = len(white) - 1
            else:
                j = len(white)

            spaces = sub_indices(white[i:j], ' ')
            m = len(spaces)

            if n > m:
                if line[0] == '#': # preprocessor
                    whitified += white[i:j+1]
                    i = j = j + 1
                else:
                    j = j + 1
            else:
                break

        indices = sorted(random.sample(spaces, n))
        groups = indices_split(white[i:j], indices)

        for k, (bit, group) in enumerate(zip(bits, groups)):
            if k > 0:
                whitified += ' ' + merge(bit, group[1:])
            else:
                whitified += merge(bit, group)

        if nl < len(lines) - 1:
            whitified += '\n'
        i = j + 1

    return restore(whitified, strings)


def main(c_file: str, white_file: str, output_file: str = None, show: bool = False) -> str:
    with open(c_file) as f, open(white_file) as g:
        code = f.read()
        white = g.read()

    code = whitifyC(code, white)

    if show:
        print(code)

    if output_file is not None:
        with open(output_file, 'w') as f:
            f.write(code)

    return code

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Whitify C file')

    parser.add_argument('input', nargs=2, help='C and Whitespace input files')
    parser.add_argument('-o', '--output', default=None, help='output file')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='print minified version on std')

    args = parser.parse_args()

    main(
        args.input[0],
        args.input[1],
        args.output,
        args.verbose
    )
