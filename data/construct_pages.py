import os
import re
import sys
import yaml
import slugify
import pytz
from dateutil.parser import parse

title_block = """---
layout: post
title:  "{title}"
date:   {date}
author: {authors}
categories: collections
---
"""

link_block = """
<div class="link_block" markdown="1">
<a href="{url}">{title}</a>
</div>"""

link_block_description = """
{description}
</div>
"""


def normalize_whitespace(source):
    """ Modified from Python Markdown. This simplifies processing of lines
    """
    start_of_text = '\u0002'  # Use STX ("Start of text") for start-of-placeholder
    end_of_text = '\u0003'  # Use ETX ("End of text") for end-of-placeholder
    source = source.replace(start_of_text, "").replace(end_of_text, "")
    source = source.replace("\r\n", "\n").replace("\r", "\n") + "\n\n"
    source = source.expandtabs(4)
    source = re.sub(r'(?<=\n) +\n', '\n', source)
    source = re.sub(r'\n\n\n+', '\n\n', source)
    return source


def process(contents):
    previous_block = None
    previous_block_is_link_block = False

    collection_title = ""
    links_data = []
    markdown_output = []

    for block in str(normalize_whitespace(contents)).split("\n\n"):
        indented = block.startswith(" " * 4)
        no_sibling = previous_block is None
        first_line = block.split("\n")[0] if len(block.split("\n")) > 0 else False
        has_type_block = first_line and first_line.lstrip().startswith("[") and first_line.rstrip().endswith("]")

        if indented and no_sibling:
            previous_block_is_link_block = False
            stripped_lines = [l.lstrip() for l in block.split("\n")]
            title, authors, date = stripped_lines[0], stripped_lines[1:-1], stripped_lines[-1]
            date = pytz.timezone('US/Pacific').localize(parse(date))
            collection_title = "{YEAR}-{MONTH}-{DAY}-{title}.md".format(
                YEAR=date.year,
                MONTH=date.month,
                DAY=date.day,
                title=slugify.slugify(title)
            )

            markdown_output.append(title_block.format(title=title, date=date.isoformat(), authors=", ".join(authors)))
        elif indented and has_type_block:
            previous_block_is_link_block = True
            stripped_lines = [l.lstrip() for l in block.split("\n")]
            yaml_block = "\n".join(stripped_lines[1:])
            yaml_data = yaml.load(yaml_block)
            links_data.append(yaml_data)

            markdown_output.append(link_block.format(title=yaml_data['title'], url=yaml_data['url']))
        elif indented and previous_block_is_link_block:
            stripped_lines = "\n".join(l.lstrip() for l in block.split("\n"))
            markdown_output[-1] = markdown_output[-1][:-6] + link_block_description.format(description=stripped_lines)
            links_data[-1]['description'] = stripped_lines
        else:
            previous_block_is_link_block = False
            markdown_output.append(block)

        previous_block = block

    return collection_title, links_data, "\n\n".join(markdown_output)


def main(filenames):
    for file in filenames:
        with open(file, 'r') as f:
            collection_title, links_data, markdown_output = process(f.read())
        with open(os.path.join("..", "_posts", collection_title), 'w') as f:
            f.write(markdown_output)


if __name__ == "__main__":
    main(sys.argv[1:])
