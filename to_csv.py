import csv
import pdb
from pprint import pprint

import requests

from config.secrets import ZENHUB_ACCESS_TOKEN

def get_github_issues(url, labels=None, state="all", per_page=100):
    res = requests.get(
        url, params={"labels": labels, "state": state, "per_page": per_page}
    )
    res.raise_for_status()
    return res.json()


def get_zenhub_issue(url, token, issue_no):
    url = f"{url}{issue_no}"
    params = {"access_token": token}
    res = requests.get(url, params=params)
    res.raise_for_status()
    return res.json()


def parse_issue(issue):
    # extract desired elements from github issue
    pipeline = issue.get("pipeline")
    title = issue.get("title")
    body = issue.get("body")
    labels = issue.get("labels")
    labels = [label["name"] for label in labels]
    number = issue.get("number")
    return {"number" : number, "pipeline": pipeline, "title": title, "labels": labels, "body": body}


def parse_labels(labels):
    # extract issue type, workgroup, and project flag from issue labels
    issue_type = None

    project = "No"

    workgroup = None

    for label in labels:

        if "workgroup" in label.lower():
            workgroup = drop_prefix(label, "Workgroup: ")

        if "type" in label.lower():
            issue_type = drop_prefix(label, "Type: ")

        if "index" in label.lower():
            project = "Yes"

    return {"project": project, "workgroup": workgroup, "type": issue_type}


def drop_prefix(val, prefix):
    # helper for parsing DTS github labels
    return val.replace(prefix, "")


def main():
    csv_data = []

    GITHUB_ENDPOINT = "https://api.github.com/repos/cityofaustin/atd-data-tech/issues"

    # 140626918 = atd-data-tech repo
    ZENHUB_ENDPOINT = "https://api.zenhub.io/p1/repositories/140626918/issues/"

    FIELDNAMES = ["number", "title", "pipeline", "workgroup", "type", "project", "body"]

    # get all "index" issues (aka, projects)
    issues = get_github_issues(GITHUB_ENDPOINT, labels="Index")

    # get all feature issues
    issues.extend(get_github_issues(GITHUB_ENDPOINT, labels="Type: Feature"))

    # get all enhancement issues
    issues.extend(get_github_issues(GITHUB_ENDPOINT, labels="Type: Enhancement"))

    for issue in issues:
        print(issue.get("number"))

        # fetch zenhub issue data
        zenhub_issue = get_zenhub_issue(
            ZENHUB_ENDPOINT, ZENHUB_ACCESS_TOKEN, issue["number"]
        )

        # add zenhub pipeline to github issue object
        try:
            issue["pipeline"] = zenhub_issue["pipeline"]["name"]

        except KeyError:
            # closed issues do not have a zenhub pipeline :(
            issue["pipeline"] = "Closed"

        # prepare issue object for csv output
        csv_issue = parse_issue(issue)

        csv_issue.update(parse_labels(csv_issue["labels"]))

        csv_issue.pop("labels")

        csv_data.append(csv_issue)

    with open("projects.csv", "w") as fout:

        writer = csv.DictWriter(fout, fieldnames=FIELDNAMES)

        writer.writeheader()

        for row in csv_data:

            writer.writerow(row)


main()
