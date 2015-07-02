import slugify
import yaml
import file_output_util


def title_block_output(title, links):
    return "---\n{}\n---".format(
        yaml.safe_dump(
            {
                "layout": "post",
                "title": title.title,
                "date": title.date,
                "author": ", ".join(title.authors),
                "categories": "collections",
                "resources": links
            },
            default_flow_style=False
        )
    )


link_block = lambda i: """
{% assign link = page.resources[~~~~~] %}
{% include link.html %}
""".replace("~~~~~", str(i))


def output(parser_output):
    collection_title = ""
    title_data = None

    output_blocks = []
    link_data = []

    for (possible_title_data, resource, text_block) in parser_output:
        if possible_title_data:
            title_data = possible_title_data
            collection_title = "{YEAR}-{MONTH}-{DAY}-{title}.md".format(
                YEAR=title_data.date.year,
                MONTH=title_data.date.month,
                DAY=title_data.date.day,
                title=slugify.slugify(title_data.title)
            )

        elif resource:
            link_data.append(resource)
            current_link_data_index = len(link_data) - 1
            output_blocks.append(link_block(current_link_data_index))

        elif text_block:
            output_blocks.append(text_block)

    if collection_title and title_data:
        file_output = "\n\n".join([title_block_output(title_data, link_data)] + output_blocks)
        file_output_util.post_file_export(file_output, collection_title)

    else:
        raise Exception("Title data not included in parser stream")
