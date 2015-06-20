
def output(parser_output):
    topics = {}

    for (_, resource, _) in parser_output:
        if resource:
            topics.setdefault(resource["topic"], []).append(resource)
