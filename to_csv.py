"""
Fetch Github issues and Zenhub metadata and write to CSV.

TODO:
- milestones
- estimates
"""

import csv
from multiprocessing.dummy import Pool
import pdb
from pprint import pprint
import time

import requests

from config.secrets import ZENHUB_ACCESS_TOKEN, GITHUB_PASSWORD, GITHUB_USER
from config.repos import REPO_LIST


def get_github_issues(url, auth, labels=None, state="open", per_page=100):

    data = []

    page = 1

    while True:

        res = requests.get(
            url,
            auth=auth,
            params={
                "labels": labels,
                "state": state,
                "per_page": per_page,
                "page": page,
            },
        )

        res.raise_for_status()

        data.extend(res.json())

        # pagination logic
        if len(res.json()) == per_page:
            page += 1
        else:
            break

    return data


def async_get_zenhub_issues(issue):
    """
    async wrapper to get zenhub issues. after creating this method i learned that 
    zenhub limits requests to 100/min. so async is basically pointless. hence we
    wait 3 seconds between each request.
    20 requests/minute * 4 workers = 80 requests/minute
    """

    # rate limited to 100 requests per second
    print(issue["number"])
    time.sleep(3)

    zenhub_endpoint = (
        f"https://api.zenhub.io/p1/repositories/{issue['repo_id']}/issues/"
    )

    # fetch zenhub issue data
    zenhub_issue = get_zenhub_issue(
        zenhub_endpoint, ZENHUB_ACCESS_TOKEN, issue["number"]
    )

    if not zenhub_issue:
        # some zenhub issues are mysteriously not found
        print("NO ZENHUB")
        issue["pipeline"] = "Unknown"
        issue["estimate"] = "Unknown"
        return issue

    # add zenhub pipeline to github issue object
    # see: https://stackoverflow.com/questions/25833613/python-safe-method-to-get-value-of-nested-dictionary
    issue["pipeline"] = zenhub_issue.get("pipeline", {}).get("name")

    if not issue.get("pipeline"):
        # closed issues do not have a zenhub pipeline :(
        issue["pipeline"] = "Closed"

    # add estimate to github issue object
    issue["estimate"] = zenhub_issue.get("estimate", {}).get("value")

    return issue


def get_zenhub_issue(url, token, issue_no):
    url = f"{url}{issue_no}"
    params = {"access_token": token}

    try:
        # handle exceptions for timeouts, connection, etc.
        res = requests.get(url, params=params)

    except requests.exceptions.Timeout:
        print("timeout")
        return None

    except:
        print("unknwon error")
        return None

    try:
        # handle status code errors
        res.raise_for_status()

    except Exception as e:
        # handle an edge cas where an issue is not found in zenub
        if res.status_code == 404:
            print(f"not found: {issue_no}")
            return None

        if res.status_code == 403:
            print(res.text)
            return None

        else:
            print(e)
            return none

    return res.json()


def parse_issue(issue):
    # extract desired elements from github issue
    pipeline = issue.get("pipeline")
    title = issue.get("title")
    title = title.replace(
        "Project: ", ""
    )  # drop the Project: xxx convention from project titles
    body = issue.get("body")
    labels = issue.get("labels")
    labels = [label["name"] for label in labels]
    number = issue.get("number")
    id_ = issue.get("id")
    repo = issue.get("repo_name")
    estimate = issue.get("estimate")
    return {
        "id": id_,
        "number": number,
        "pipeline": pipeline,
        "title": title,
        "labels": labels,
        "body": body,
        "repo": repo,
        "estimate": estimate,
    }


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

    issues = []

    csv_data = []

    for repo in stu:
        # iterate through all the repos to get issuse of interest
        repo_name = repo.get("name")

        repo_id = repo.get("id")

        github_endpoint = (
            f"https://api.github.com/repos/cityofaustin/{repo_name}/issues"
        )

        print(repo.get("name"))

        """
        nixing this index-specific query for now. if we want closed Index issues, we'll need to do this
        and also remove dupes from the existing query

        if repo.get("name") == "atd-data-tech":
            # this is the only repo that should have "Index" issues (aka, Projects),
            # and we want all of them (including closed)
            issues.extend(get_github_issues(github_endpoint, labels="Index", state="all"))
        """

        # get all open issues
        append_issues = get_github_issues(
            github_endpoint, (GITHUB_USER, GITHUB_PASSWORD)
        )

        # and repo info to each issue
        for issue in append_issues:
            issue["repo_name"] = repo_name
            issue["repo_id"] = repo_id

        issues.extend(append_issues)

    with Pool(processes=4) as pool:
        # async get zenhub pipeline attributes
        issues = pool.map(async_get_zenhub_issues, issues)

    for issue in issues:
        # prepare issue object for csv output
        csv_issue = parse_issue(issue)

        csv_issue.update(parse_labels(csv_issue["labels"]))

        csv_issue.pop("labels")

        csv_data.append(csv_issue)

    with open("projects.csv", "w") as fout:

        FIELDNAMES = [
            "id",
            "number",
            "title",
            "pipeline",
            "workgroup",
            "type",
            "project",
            "body",
            "repo",
            "estimate",
        ]

        writer = csv.DictWriter(fout, fieldnames=FIELDNAMES)

        writer.writeheader()

        for row in csv_data:

            writer.writerow(row)


main()
