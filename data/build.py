import sys
import yaml
import sqlite3
import os
import csv
import shutil
from collections import OrderedDict

export_sql = """
	SELECT title,date_written,link.url, source.url as 'source_url' 
	FROM link left join source on link.source_id = source.id
	WHERE link.topic_id = ?;
"""

category_page_data = """---
||---
<ul class="category_listing">
	{% for link in site.data.++++ %}
	  {% include category_listing.html %}
	{% endfor %}
</ul>
"""

def export_csv_page_data(c, data_dir, topic_id, topic_stack_joined):
	rows = []
	for row in c.execute(export_sql, [topic_id]):
		if len(rows) == 0:
			rows.append(list(row.keys()))
		rows.append(row)
	with open(os.path.join(data_dir, topic_stack_joined + ".csv"), 'w') as f:
		csv.writer(f).writerows(rows)

def export_page_data(category_name, category_id, category_stack, category_stack_joined):
	metadata = dict(
		title=category_name,
		category_name=category_name,
		category_stack=category_stack,
		layout="default"
	)
	return category_page_data.replace(
		"||", yaml.safe_dump(dict(**metadata))
		).replace(
		"++++", category_stack_joined
		)

def setup():
	conn = sqlite3.connect(sys.argv[1])
	conn.row_factory = sqlite3.Row
	return conn.cursor()

def make_topic_tree(c):
	topic_tree = OrderedDict()
	topic_links = OrderedDict()
	topic_names = OrderedDict()
	for (id, name, parent_id) in c.execute('SELECT * FROM topic'):
		id = int(id)
		parent_id = int(parent_id) if parent_id else None
		if not parent_id:
			topic_links[id] = {}
			topic_tree[id] = topic_links[id]
			topic_names[id] = name
		else:
			topic_links[id] = {}
			topic_links[parent_id][id] = topic_links[id]
			topic_names[id] = name

	return topic_tree, topic_links, topic_names

def export_tree(topic_id, topic_stack, topic_tree, topic_names, c, data_dir):
	try:
		os.mkdir(topic_names[topic_id])
	except FileExistsError:
		shutil.rmtree(topic_names[topic_id])
		os.mkdir(topic_names[topic_id])
	os.chdir(topic_names[topic_id])

	topic_stack_joined = "_".join(topic_stack)
	export_csv_page_data(c, data_dir, topic_id, topic_stack_joined)

	with open('index.html', 'w') as f:
		f.write(export_page_data(topic_names[topic_id], topic_id, topic_stack, topic_stack_joined))
	for child in topic_tree.get(topic_id, {}):
		child_name = topic_names[child]
		export_tree(child, topic_stack + (child_name,), topic_tree, topic_names, c, data_dir)
	os.chdir('..')


def main():
	c = setup()
	(topic_tree, topic_links, topic_names) = make_topic_tree(c)
	os.chdir('..')
	try:
		os.mkdir("_data")
	except FileExistsError:
		pass
	data_dir = os.path.abspath(os.path.join('.', '_data'))
	for topic_id in topic_tree:
		export_tree(topic_id, (topic_names[topic_id],), topic_tree, topic_names, c, data_dir)

if __name__ == "__main__":
	main()
