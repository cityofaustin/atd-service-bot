# TODO:
# validator/checker
# assignments
# update knack issue with github link
# udpate knack issue with migration status

import pdb
from pprint import pprint as print

from knackpy import Knack

from config.config import *
from config.secrets import API_KEY
import transforms

# def validate_issue_payload(issue, field_definitions):


kn = Knack(
    scene=KNACK_APP["scene"],
    view=KNACK_APP["view"],
    app_id=KNACK_APP["app_id"],
    api_key=API_KEY,
    ref_obj=KNACK_APP["ref_obj"],
)

prepared = []

for row in kn.data:
    github_issue = {
        "description": "",
        "labels": [],
        "title": "",
        "assignee": None,
        "github_url": None,
        "knack_id": None,
        "repo": None,
    }

    for field in FIELDS:
        if field["method"] == "merge":
            old_value = github_issue[field["github"]]

            try:
                new_value = f"{old_value}{field['knack']}: {row[field['knack']]}\n\n"

            except KeyError:
                continue

            github_issue[field["github"]] = new_value

        elif field["method"] == "transform_merge":
            try:
                untransformed = row[field["knack"]]

            except KeyError:
                continue

            # get the transform function
            transform_func = getattr(transforms, field["transform"])
            transformed = transform_func(untransformed)

            # now merge
            old_value = github_issue[field["github"]]
            new_value = f"{old_value} {field['knack']}: {transformed}\n\n"
            github_issue[field["github"]] = new_value

        elif field["method"] == "map_append":

            try:
                val_knack = row[field["knack"]]

            except KeyError:
                continue

            val_mapped = field["map"][val_knack]

            github_issue[field["github"]].append(val_mapped)

        elif field["method"] == "map":

            try:
                val_knack = row[field["knack"]]

            except KeyError:
                continue

            val_mapped = field["map"][val_knack]
            github_issue[field["github"]] = val_mapped
      
        elif field["method"] == "copy":

            try:
                val_knack = row[field["knack"]]

            except KeyError:
                continue

            github_issue[field["github"]] = val_knack

    pdb.set_trace()

    prepared.append(github_issue)

pdb.set_trace()
