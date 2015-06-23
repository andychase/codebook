#!/usr/local/bin/python3
import os
import sys

import export_posts
import export_topics
import parser


def main(arguments):
    for arg in arguments:
        if os.path.isdir(arg):
            arg = [os.path.join(arg, f) for f in os.listdir(arg)]
        else:
            arg = [arg]

        for file in arg:
            with open(file, 'r') as f:
                page_output = list(parser.process(f.read()))

        export_posts.output(page_output)
        export_topics.output(page_output)


if __name__ == "__main__":
    main(sys.argv[1:])
