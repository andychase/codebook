from itertools import chain
import os
import slugify

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
<div class="icon {icon}"></div>
<a href="{url}">{title}</a><span class="domain">({domain})</span>

{description}

</div>
"""

type_icon_map = {
    "guide": "ss-signpost"
}

output_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "_posts"))


def get_first_and_return_full(iterator):
    value = next(iterator)
    return value, chain([value], iterator)


def output(parser_output):
    first_output, parser_output = get_first_and_return_full(parser_output)
    info, _, _ = first_output
    collection_title = "{YEAR}-{MONTH}-{DAY}-{title}.md".format(
        YEAR=info.date.year,
        MONTH=info.date.month,
        DAY=info.date.day,
        title=slugify.slugify(info.title)
    )
    with open(os.path.join(output_dir, collection_title), 'w') as f:
        for (title, resource, text_block) in parser_output:
            if title:
                f.write(
                    title_block.format(
                        title=title.title,
                        date=title.date.isoformat(),
                        authors=", ".join(title.authors))
                )
            elif resource:
                f.write(link_block.format(
                    title=resource.title,
                    icon=type_icon_map[resource.type],
                    domain=resource.domain,
                    url=resource.url,
                    description=resource.description
                ))
            elif text_block:
                f.write(text_block)
            f.write("\n\n")
