#!/usr/local/bin/python3
""" Usage: python3 construct_pages.py <input directory>

The construct_pages.py utility takes a directory of Codebook collection pages and exports
cleaned up and processed markdown in site/_posts/ and site/_topics/ directories.

All arguments after the first are ignored (this is for use with fswatch and xargs).
"""
import os
import sys

import export_posts
import export_topics
import parser


def main(arg):
    page_data = []
    if not os.path.isdir(arg):
        return print("Argument not a valid directory!\n\n{}".format(__doc__))

    for file in os.listdir(arg):
        if file.startswith("."):
            continue
        file_path = os.path.join(arg, file)

        with open(file_path, 'r') as f:
            page_output = list(parser.process(f.read()))

        export_posts.output(page_output)
        page_data += page_output

    export_topics.output(page_data)


def cli():
    if len(sys.argv) < 2:
        print(__doc__)
    else:
        main(sys.argv[1])


if __name__ == "__main__":
    cli()
