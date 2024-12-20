import os
from collections.abc import Iterable


def read_input(day, transformer=str, example=False):
    """
    Given a day number (1-25), reads the corresponding input file into
    a list and runs a transformer function against each item in the list.
    """
    try:
        if example:
            filename = f'day_{day}_example.txt'
        else:
            filename = f'day_{day}.txt'
        with open(os.path.join('inputs', filename)) as input_file:
            return [transformer(line.strip()) for line in input_file]
    except FileNotFoundError as e:
        print(e)


def read_multisection_input(day, transformers, example=False):
    """
    Given a day number (1-25), reads the corresponding input file, splits by empty line
    and runs a transformer function from `transformers` list for each section and returns
    a list of section outputs
    """
    try:
        if example:
            filename = f'day_{day}_example.txt'
        else:
            filename = f'day_{day}.txt'
        with open(os.path.join('inputs', filename)) as input_file:
            output = []
            sections = input_file.read().split('\n\n')
            if transformers:
                for idx, section in enumerate(sections):
                    output.append(transformers(section))
            else:
                output = sections
            return output
    except FileNotFoundError as e:
        print(e)


def read_stream(day, transformer=str, example=False):
    """
    Given a day number (1-25), reads the corresponding input file into
    a string and runs a transformer function against it.
    """
    try:
        if example:
            filename = f'day_{day}_example.txt'
        else:
            filename = f'day_{day}.txt'
        with open(os.path.join('inputs', filename)) as input_file:
            return transformer(input_file.read())
    except FileNotFoundError as e:
        print(e)


def flatten(x):
    if isinstance(x, Iterable):
        return [a for i in x for a in flatten(i)]
    else:
        return [x]
