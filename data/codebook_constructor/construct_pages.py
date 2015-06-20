#!/usr/local/bin/python3
import sys

import export_posts
import export_topics
import parser


def main(filenames):
    for file in filenames:
        with open(file, 'r') as f:
            page_output = list(parser.process(f.read()))

        export_posts.output(page_output)
        export_topics.output(page_output)


if __name__ == "__main__":
    main(sys.argv[1:])
