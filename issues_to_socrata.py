#!/usr/bin/env python3
"""
Fetch Github issues and Zenhub metadata and publish to open data portal
"""
import datetime
import logging
import os
import sys

from github import Github
import requests
import sodapy

REPO = {"id": 140626918, "name": "cityofaustin/atd-data-tech"}
WORKSPACE_ID = "5caf7dc6ecad11531cc418ef"
SOCRATA_RESOURCE_ID = os.environ["SOCRATA_RESOURCE_ID"]
ZENHUB_ACCESS_TOKEN = os.environ["ZENHUB_ACCESS_TOKEN"]
GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
SOCRATA_ENDPOINT = os.environ["SOCRATA_ENDPOINT"]
SOCRATA_API_KEY_ID = os.environ["SOCRATA_API_KEY_ID"]
SOCRATA_API_KEY_SECRET = os.environ["SOCRATA_API_KEY_SECRET"]
SOCRATA_APP_TOKEN = os.environ["SOCRATA_APP_TOKEN"]

def extract_workgroups_from_labels(labels):
    """Extract a comma-separated list of workgroup names from "Workgroup: Xyz" labels"""
    workgroup_labels = list(
        set([label.name for label in labels if label.name.startswith("Workgroup:")])
    )
    workgroup_labels_no_prefix = [
        label.replace("Workgroup:", "").strip() for label in workgroup_labels
    ]
    return ", ".join(workgroup_labels_no_prefix) or None


def get_github_issues(repo_name, github_access_token, state="all"):
    g = Github(github_access_token)
    repo = g.get_repo(repo_name)
    issues_metadata = repo.get_issues(state=state)
    return [issue for issue in issues_metadata]


def issue_to_dict(issue):
    """breakdown pygithub classes into dicts"""
    issue_dict = {}

    issue_dict["workgroups"] = extract_workgroups_from_labels(issue.labels)

    issue_dict["labels"] = ", ".join([label.name for label in issue.labels])

    issue_dict["milestone"] = (
        None if not getattr(issue, "milestone") else issue.milestone.title
    )

    for attr in [
        "title",
        "body",
        "closed_at",
        "created_at",
        "updated_at",
        "state",
        "number",
        "id",
        "url",
    ]:
        issue_dict[attr] = getattr(issue, attr)
    return issue_dict


def convert_timestamps(issues):
    for issue in issues:
        for key, val in issue.items():
            if isinstance(val, datetime.datetime):
                issue[key] = val.isoformat()


def get_zenhub_metadata(workspace_id, token, repo_id, timeout=60):
    url = f"https://api.zenhub.com/p2/workspaces/{workspace_id}/repositories/{repo_id}/board"
    params = {"access_token": token}
    res = requests.get(url, params=params, timeout=timeout)
    res.raise_for_status()
    return res.json()


def create_zenhub_metadata_index(metadata):
    """flatten the zenhub metadata so that we can lookup issue properties by number"""
    index = {}
    for p in metadata["pipelines"]:
        pipeline_name = p["name"]
        for issue in p["issues"]:
            issue_number = issue["issue_number"]
            index[issue_number] = {
                "is_epic": issue["is_epic"],
                "position": issue["position"],
                "estimate": issue.get("estimate", {}).get("value"),
                "pipeline": pipeline_name,
            }
    return index


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def main():
    logging.info("Fetching github issues...")
    issues_gh = get_github_issues(REPO["name"], GITHUB_ACCESS_TOKEN)
    issues = [issue_to_dict(issue) for issue in issues_gh]

    logging.info("Converting timestamps...")
    convert_timestamps(issues)

    logging.info("Fetching zenhub data...")
    zenhub_metadata = get_zenhub_metadata(WORKSPACE_ID, ZENHUB_ACCESS_TOKEN, REPO["id"])
    zenhub_metadata_index = create_zenhub_metadata_index(zenhub_metadata)

    logging.info("Processing Zenhub data...")
    for issue in issues:
        zenhub_meta = zenhub_metadata_index.get(issue["number"])
        if zenhub_meta:
            issue.update(zenhub_meta)

        # set pipeline for closed issues, which have no pipeline metadata
        issue["pipeline"] = (
            "Closed" if issue["state"] == "closed" else issue.get("pipeline")
        )

    client = sodapy.Socrata(
        SOCRATA_ENDPOINT,
        SOCRATA_APP_TOKEN,
        username=SOCRATA_API_KEY_ID,
        password=SOCRATA_API_KEY_SECRET,
        timeout=60,
    )

    logging.info(f"Uploading to Socrata...")
    first_chunk = True
    for chunk in chunks(issues, 1000):
        if first_chunk:
            # completely replace dataset to ensure deleted issues are flushed
            client.replace(SOCRATA_RESOURCE_ID, issues)
            first_chunk = False
        client.upsert(SOCRATA_RESOURCE_ID, issues)
        logging.info(f"{len(chunk)} processed")


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main()
