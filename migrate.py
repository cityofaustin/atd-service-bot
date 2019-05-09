# TODO:
# validator/checker
# assignments
# update knack issue with github link
# udpate knack issue with migration status

import pdb
from pprint import pprint as print

from github import Github
from knackpy import Knack

from config.config import *
from config.secrets import API_KEY, GITHUB_USER, GITHUB_PASSWORD
import transforms

# def validate_issue_payload(issue, field_definitions):

def map_issue(issue, FIELDS):
    
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
                new_value = f"{old_value}{field['knack']}: {issue[field['knack']]}\n\n"

            except KeyError:
                continue

            github_issue[field["github"]] = new_value

        elif field["method"] == "transform_merge":
            try:
                untransformed = issue[field["knack"]]

            except KeyError:
                continue

            # get the transform function
            transform_func = getattr(transforms, field["transform"])
            transformed = transform_func(untransformed)

            # now merge
            old_value = github_issue[field["github"]]


            if field.get('rename'):
                # rename the field label that will be formatted into the merge
                new_value = f"{old_value}{field.get('rename')}: {transformed}\n\n"

            else:
                new_value = f"{old_value}{field['knack']}: {transformed}\n\n"
            
            github_issue[field["github"]] = new_value

        elif field["method"] == "map_append":

            try:
                val_knack = issue[field["knack"]]

            except KeyError:
                continue
            
            if not val_knack:
                # handle empty strings in knack data
                continue
            
            if field.get("splice_by_comma") and "," in val_knack:
                # handle a field with multiple, comma-delimmited values
                val_knack = val_knack.split(",")

            else:
                val_knack = [val_knack]

            for val in val_knack:
                val_mapped = field["map"][val]
                
                github_issue[field["github"]].append(val_mapped)
            

        elif field["method"] == "map":

            try:
                val_knack = issue[field["knack"]]

            except KeyError:
                if field.get("default"):
                    github_issue[field["github"]] = field.get("default")

                continue

            if not val_knack:
                # skip empty strings in knack data
                if field.get("default"):
                    github_issue[field["github"]] = field.get("default")
                    
                continue
            
            val_mapped = field["map"][val_knack]

            github_issue[field["github"]] = val_mapped
      
        elif field["method"] == "copy":

            try:
                val_knack = issue[field["knack"]]

            except KeyError:
                continue

            github_issue[field["github"]] = val_knack

    return github_issue
    

def get_repo(g, repo, org="cityofaustin"):
    return g.get_repo(f"{org}/{repo}")


kn = Knack(
    scene=KNACK_APP["scene"],
    view=KNACK_APP["view"],
    app_id=KNACK_APP["app_id"],
    api_key=API_KEY,
    ref_obj=KNACK_APP["ref_obj"],
)

prepared = {}

count = 0
for issue in kn.data:

    # turn knack issues into github iossues
    github_issue = map_issue(issue, FIELDS)
    
    # organize issues by repo
    repo = github_issue['repo']
    
    if repo not in prepared:
        prepared[repo] = []

    prepared[repo].append(github_issue)

    # create github issues
    # for repo in prepared.keys():
    #     for issue in prepared[repo]:
    #         print(issue['title'])

# g = Github(GITHUB_USER, GITHUB_PASSWORD)
pdb.set_trace()
