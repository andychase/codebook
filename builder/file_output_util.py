import os


output_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "site"))
topic_output_dir = os.path.join(output_dir, "_topics")
post_output_dir = os.path.join(output_dir, "_posts")
top_links_output_dir = os.path.join(output_dir, "_data")

for directory in (topic_output_dir, post_output_dir, top_links_output_dir):
    if not os.path.isdir(directory):
        os.mkdir(directory)

max_ten_megabytes = 1024 * 1024


def write_file_if_different(file_path, output_data):
    """ This function checks an existing file and skips writing to it
        if the file's contains is no different then the pending changes.

        The reason for this is so Jekyll doesn't have to regenerate the files
        if there aren't any changes.
    """
    if os.path.isfile(file_path):
        with open(file_path) as f:
            if f.read(max_ten_megabytes) == output_data:
                return
    with open(file_path, 'w') as f:
        f.write(output_data)


def post_file_export(file_output, collection_title):
    write_file_if_different(os.path.join(post_output_dir, collection_title), file_output)


def topic_file_export(file_output, topic_file_name):
    write_file_if_different(os.path.join(topic_output_dir, topic_file_name), file_output)


def top_links_file_export(file_output):
    write_file_if_different(os.path.join(top_links_output_dir, "top_links.yml"), file_output)
