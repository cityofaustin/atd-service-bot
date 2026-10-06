"""
Updates the Division issue field for Epics and Tasks in atd-data-tech based on the Workgroup labels

python update_issue_task.py --type "epic"
or 
python update_issue_task.py --type "task"

Github issue: https://github.com/cityofaustin/atd-data-tech/issues/28739

"""

import requests
import logging
import sys
import os
import argparse

from secrets import GITHUB_ACCESS_TOKEN

GITHUB_ENDPOINT = "https://api.github.com/graphql"
# GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]
headers = {
    "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
    "Accept": "application/vnd.github+json",
}

workgroups = {
    "Workgroup: ACME": "",  # no mapping, 2 issues exist
    "Workgroup: ATS": "",  # no mapping, 88 issues exist
    "Workgroup: TPW": "TPW",
    "Workgroup: ATSD": "ATSD",
    "Workgroup: AMD": "AMD",
    "Workgroup: CCO": "CCG",
    "Workgroup: CPO": "SP",
    "Workgroup: CSD": "CSD",
    "Workgroup: District Maintenance": "DM",
    "Workgroup: DTS": "DTS",
    "Workgroup: Emergency Management": "EM",
    "Workgroup: Enforcement Services": "PE",
    "Workgroup: Equity": "Equity",
    "Workgroup: Finance": "Finance",
    "Workgroup: HR": "HR",
    "Workgroup: Land Development Engineering": "LDE",
    "Workgroup: LDE": "LDE",
    "Workgroup: Logistics": "Logistics",
    "Workgroup: Mobility Services": "PE",
    "Workgroup: OCE": "OCE",
    "Workgroup: OOD": "TPW",
    "Workgroup: OPM": "OPM",
    "Workgroup: OSE": "OSE",
    "Workgroup: Parking Services": "PE",
    "Workgroup: Pavement Operations": "PO",
    "Workgroup: PDD": "PD",
    "Workgroup: PIO": "PIO",
    "Workgroup: ROW": "ROW",
    "Workgroup: SBO": "SBO",
    "Workgroup: SDD": "SDD",
    "Workgroup: SMD": "SMD",
    "Workgroup: SMO": "CSD",
    "Workgroup: SMS": "PE",
    "Workgroup: SPP": "SP",
    "Workgroup: SUTD": "SUTD",
    "Workgroup: TDS": "TDS",
    "Workgroup: TED": "TED",
    "Workgroup: Urban Forestry": "UF",
    "Workgroup: Utilities & Structures": "US",
    "Workgroup: VZ": "VZ",
}


def get_issues(issue_type):
    url = f"https://api.github.com/repos/cityofaustin/atd-data-tech/issues"
    params = {"per_page": 100, "state": "closed", "type": issue_type}
    issues = []
    while url:
        logging.info(f"getting {url}")
        r = requests.get(url, headers=headers, params=params)
        issues.extend(r.json())
        url = r.links.get("next", {}).get("url")  # handle pagination
        params = {}  # don't re-send params on paginated URLs
    return issues


def has_divisions_github_field(issue):
    if issue.get("issue_field_values"):
        field_values = issue.get("issue_field_values")
        for field in field_values:
            if field.get("issue_field_id") == 44588370:
                logging.info(
                    f"- {issue['number']} divisions are already {field.get('value')}"
                )
                return True
    return False


def get_list_of_workgroups_labels(issue):
    all_labels = issue.get("labels")
    divisions_on_issue = []
    for label in all_labels:
        label_name = label.get("name")
        if label_name in workgroups.keys():
            if label_name == "Workgroup: ACME" or label_name == "Workgroup: ATS":
                continue
            divisions_on_issue.append(workgroups[label_name])
    return divisions_on_issue


def update_issue_field_divisions(issue_number, divisions):
    endpoint = f"https://api.github.com/repos/cityofaustin/atd-data-tech/issues/{issue_number}/issue-field-values"
    issue_field_values = []
    issue_field_values.append({"field_id": 44588370, "value": divisions})
    res = requests.post(
        endpoint, json={"issue_field_values": issue_field_values}, headers=headers
    )
    res.raise_for_status()
    # logging.info(res)


def main(args):
    # issue_type = args.type
    issue_type = "task"
    if issue_type not in ["epic", "task"]:
        raise ValueError(f"{issue_type} needs to be either task or epic.")
    all_issues = get_issues(issue_type)
    logging.info(f"Total issues: {len(all_issues)}")


    updated = 0

    for issue in all_issues:
        issue_number = issue.get("number")
        # this is the cursed issue that wont let me update it
        if issue_number == "4189" or issue_number == 4189:
            logging.info(type(issue_number))
            continue
        # if we already have the division issue field defined, just skip it
        if has_divisions_github_field(issue):
            continue
        divisions = get_list_of_workgroups_labels(issue)
        logging.info(f"{issue_number}: {divisions}")
        if divisions:
            updated += 1
            update_issue_field_divisions(issue_number, divisions)

    logging.info(updated)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = argparse.ArgumentParser(
        description="Batch-update GitHub team issue field."
    )
    # parser.add_argument("--type", required=True, help="issue type, epic or task")
    args = parser.parse_args()
    main(args)
