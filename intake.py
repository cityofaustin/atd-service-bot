# TODO: handle "other" division, request type
# TODO: map to geospatial—document
# TODO: document geospatial app selection importance
# TODO: document why email/name are short text
# TODO: test: all apps, all request types, all divisions
# TODO: test default assignees
# TODO: attachment

import pdb
from pprint import pprint as print

from github import Github
import knackpy

from config.config import KNACK_APP, FIELDS
from config.secrets import API_KEY, GITHUB_USER, GITHUB_PASSWORD
import _transforms


def get_service_requests(knack_config, api_key):
    # Just a wrapper. Returns a Knackpy object.

    return knackpy.Knack(
        scene=knack_config["scene"],
        view=knack_config["view"],
        app_id=knack_config["app_id"],
        api_key=api_key,
        ref_obj=knack_config["ref_obj"],
    )


def map_issue(issue, fields, knack_field_map):

    github_issue = {
        "description": "",
        "labels": [],
        "title": "",
        "github_url": None,
        "knack_id": None,
        "repo": None,
    }

    for field in fields:

        knack_field_label = knack_field_map[field["knack"]]["label"]

        if field["method"] == "merge":
            old_value = github_issue[field["github"]]

            try:
                if not issue[knack_field_label]:
                    continue

                new_value = (
                    f"{old_value}{knack_field_label}: {issue[knack_field_label]}\n\n"
                )

                github_issue[field["github"]] = new_value

            except KeyError:
                continue

        elif field["method"] == "transform_merge":

            try:
                if not issue[knack_field_label]:
                    continue

                untransformed = issue[knack_field_label]

            except KeyError:
                continue

            # get the transform function
            transform_func = getattr(_transforms, field["transform"])
            transformed = transform_func(untransformed)

            # now merge
            old_value = github_issue[field["github"]]

            if field.get("rename"):

                # rename the field label that will be formatted into the merge
                new_value = f"{old_value}{field.get('rename')}: {transformed}\n\n"

            else:
                new_value = f"{old_value}{knack_field_label}: {transformed}\n\n"

            github_issue[field["github"]] = new_value

        elif field["method"] == "map_append":

            try:
                val_knack = issue[knack_field_label]

            except KeyError:
                continue

            if not val_knack:
                # handle empty strings in knack data
                continue

            else:
                val_knack = [val_knack]

            for val in val_knack:
                val_mapped = field["map"][val]

                github_issue[field["github"]].append(val_mapped)

        elif field["method"] == "map":

            try:
                if not issue[knack_field_label]:
                    continue

                val_knack = issue[knack_field_label]

            except KeyError:
                if field.get("default"):
                    github_issue[field["github"]] = field.get("default")

                continue

            val_mapped = field["map"][val_knack]

            github_issue[field["github"]] = val_mapped

        elif field["method"] == "copy":

            try:
                # we try/except here to handle empty/optional fields
                if not issue[knack_field_label]:
                    continue

                val_knack = str(issue[knack_field_label]) + "\n\n"

            except KeyError:
                continue

            github_issue[field["github"]] = val_knack

    return github_issue


def assign_to_someone(issue, repo):
    if repo == "atd-geospatial":
        issue["assignee"] = "jaime-mckeown"
    else:
        issue["assignee"] = ["amenity", "TracyLinder"]

    return issue


def get_repo(g, repo, org="cityofaustin"):
    return g.get_repo(f"{org}/{repo}")


def main():

    issues = get_service_requests(KNACK_APP, API_KEY)

    prepared = {}

    for issue in issues.data:

        # turn knack issues into github issues
        github_issue = map_issue(issue, FIELDS, issues.fields)

        # organize issues by repo
        repo = github_issue["repo"]

        github_issue = assign_to_someone(github_issue, repo)

        if repo not in prepared:
            prepared[repo] = []

        prepared[repo].append(github_issue)

    g = Github(GITHUB_USER, GITHUB_PASSWORD)

    responses = []

    # create github issues
    for repo_name in prepared.keys():

        repo = get_repo(g, repo_name)

        for issue in prepared[repo_name]:

            result = repo.create_issue(
                title=issue["title"],
                labels=issue.get("labels"),
                assignees=issue.get("assignee"),
                body=issue["description"],
            )

            pdb.set_trace()

            knack_record_update = {
                "id": issue["knack_id"],
                "field_367": result.number,  # github issuer number
                "field_368": repo_name,  # repo name
                "field_366": "Successful",  # github migration result
            }

            response = knackpy.record(
                knack_record_update,
                obj_key="object_6",
                app_id=KNACK_APP["app_id"],
                api_key=API_KEY,
                method="update",
            )

            responses.append(response)


main()
