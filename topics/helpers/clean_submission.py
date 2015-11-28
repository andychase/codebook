import json
from typing import List, Dict, Union
import bleach

allowed_items = {
    "section", "subsection", "link"
}

allowed_sub_items = {
    "title",
    "url",
    "metadata",
    "desc",
    "commentary"
}


def clean_submission(upload_post: str) -> List[Union[str, Dict[str, str]]]:
    output = []
    for resource in json.loads(upload_post):
        for key, value in resource.items():
            if key in allowed_items:
                included_item = {}
                if key == "link":
                    for link_key, link_value in value.items():
                        if link_key in allowed_sub_items:
                            included_item[link_key] = bleach.clean(link_value)
                else:
                    included_item = bleach.clean(value)
                output.append({key: included_item})
    return output
