import csv
import pdb
from pprint import pprint

import requests

from config.secrets import ZENHUB_ACCESS_TOKEN

from config.repos import REPO_LIST

def get_github_issues(url, labels=None, state="open", per_page=100):

    data = []

    page = 1

    while True:
        
        res = requests.get(
            url, params={"labels": labels, "state": state, "per_page": per_page, "page" : page}
        )
    
        res.raise_for_status()

        data.extend(res.json())

        # pagination logic
        if len(res.json()) == per_page:
            page += 1
        else:
            break

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
    repo = issue.get("repo")
    return {"number" : number, "pipeline": pipeline, "title": title, "labels": labels, "body": body, "repo": repo}


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

    issues = []
    for repo in REPO_LIST:
        # iterate through all the repos to get issuse of interest
        repo_name = repo.get("name")

        github_endpoint = f"https://api.github.com/repos/cityofaustin/{repo_name}/issues"

        ZENHUB_ENDPOINT = f"https://api.zenhub.io/p1/repositories/{repo['id']}/issues/"

        print(repo.get("name"))

        '''
        nixing this index-specific query for now. if we want closed Index issues, we'll need to do this
        and also remove dupes from the existing query

        if repo.get("name") == "atd-data-tech":
            # this is the only repo that should have "Index" issues (aka, Projects),
            # and we want all of them (including closed)
            issues.extend(get_github_issues(github_endpoint, labels="Index", state="all"))
        '''

        # get all open issues
        append_issues = get_github_issues(github_endpoint)

        for issue in append_issues:
            issue["repo"] = repo_name
        
        issues.extend(append_issues)

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
        
        FIELDNAMES = ["number", "title", "pipeline", "workgroup", "type", "project", "body", "repo"]

        writer = csv.DictWriter(fout, fieldnames=FIELDNAMES)

        writer.writeheader()

        for row in csv_data:

            writer.writerow(row)


main()
