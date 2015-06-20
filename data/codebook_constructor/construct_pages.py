#!/usr/local/bin/python3
import sys

from export import output
from parser import process


def main(filenames):
    for file in filenames:
        with open(file, 'r') as f:
            output(process(f.read()))


if __name__ == "__main__":
    main(sys.argv[1:])
