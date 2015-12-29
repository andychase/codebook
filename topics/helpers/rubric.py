import yaml

rubric = yaml.load("""
type:
    - news -- News
    - opinion -- Essay/Opinion -- A long opinion piece
    - story -- Essay/Story
    - data -- Data
    - tool -- Tool
    - list -- List
    - guide -- Guide
    - demo -- Demo

difficulty:
    - 1 -- Anyone can read
    - 2 -- Some jargon
    - 3 -- More in-depth
    - 4 -- Some knowledge is assumed
    - 5 -- Extensive expert knowledge is required

quality:
    - 1 -- Incomprehensible wall of text
    - 2 -- Contains useful information under a layer of fluff
    - 3 -- Very readable
    - 4 -- Interesting, insightful / Compelling
    - 5 -- Brings the topic to life

""")
for list_type in rubric:
    rubric[list_type] = [i.split(" -- ") for i in rubric[list_type]]
