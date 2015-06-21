import os
import yaml
from collections import namedtuple, defaultdict

TopicNode = namedtuple("TopicNode", "subtopics resources")
new_topic_tree = lambda: defaultdict(lambda: TopicNode(new_topic_tree(), []))

output_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "_topics"))


def metadata_block_output(level, current, subcategories, parents, all_topics):
    mid_link_part = "/".join(list(parents) + [":title"]) + "/"
    permalink = "/:collection/{}".format(mid_link_part)
    path = parents + (current,)
    categories = list(build_category_listing(all_topics, path))
    if any(subcategories):
        categories.append([path + (c,) for c in subcategories])
    resources = get_leaf_node(all_topics, path).resources

    return "---\n{}\n---".format(
        yaml.safe_dump(
            {
                "title": current,
                "layout": "subcategory",
                "permalink": permalink,
                "level": level,
                "nav_active": path,
                "categories": categories,
                "resources": resources
            },
            default_flow_style=False
        )
    )


def get_siblings_at(topics, path):
    if len(path) == 1:
        return list(topics[path[0]].subtopics.keys())
    else:
        return get_siblings_at(topics[path[0]].subtopics, path[1:])


def get_leaf_node(topics, path):
    if len(path) == 1:
        return topics[path[0]]
    else:
        return get_leaf_node(topics[path[0]].subtopics, path[1:])


def build_category_listing(topics, path_parts):
    for depth in range(1, len(path_parts)):
        yield [path_parts[:depth] + (t,) for t in get_siblings_at(topics, path_parts[:depth])]


def export_topics(all_topics, current_topics, parents=(), level=1):
    for topic_name, node in current_topics.items():
        file_name = "_".join(parents + (topic_name,)) + ".md"

        with open(os.path.join(output_dir, file_name), 'w') as f:
            f.write(metadata_block_output(level, topic_name, list(node.subtopics.keys()), parents, all_topics))

        export_topics(all_topics, node.subtopics, parents + (topic_name,), level=level+1)


def output(parser_output):
    topics = new_topic_tree()

    for (_, resource, _) in parser_output:
        if resource:
            topic_parts = tuple(resource["topic"].strip("/").split("/"))

            leaf = get_leaf_node(topics, topic_parts)
            leaf.resources.append(resource)

    export_topics(topics, topics)
