echo ".mode csv
.import author.csv author
.import person.csv person
.import source.csv source
.import topic.csv topic
.import link.csv link
.import review.csv review
.import tag.csv tag" | sqlite3 db.db
python3 build.py db.db
rm db.db
