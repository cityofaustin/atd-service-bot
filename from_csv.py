"""
Create Github issues from a CSV.

** Usage **

1. TO AVOID UNEXPECTED RESULTS we recommend testing this process with a single
issue, then adding additional issues after success.

2. Create a file called `issues.csv` with these exact column names:
    - `repo`
        The respository name, in the format {org}/{repo-name}. E.g. `cityofaustin/atd-data-tech`
    - `title`
        The issue title
    - `description`
        The issue description.
    - `labels`
        Each label to be applied to the issue, separated by a comma. The label
        names must *exactly match* an existing label in the destination repo.
    - `assignees`
        The github username of the person to which the issue should be assigned.
        This is case sensitive. For multiple assignees, separate each username
        with a comma.

3. Populate your file with one issue per row and save it in the same directory as this script.

4. Run the script. Tada!
"""
import csv
import os

from github import Github


def parse_list(values):
    return [val.strip() for val in values.split(",")]


def main():
    GITHUB_ACCESS_TOKEN = os.environ["GITHUB_ACCESS_TOKEN"]

    with open("issues.csv", "r") as fin:
        reader = csv.DictReader(fin)
        data = [row for row in reader]

    g = Github(GITHUB_ACCESS_TOKEN)

    current_repo = ""

    success = 0
    fail = 0

    for row in data:

        repo = row.get("repo")

        if repo != current_repo:
            current_repo = repo
            r = g.get_repo(current_repo)

        issue = {
            "title": row.get("title"),
            "labels": parse_list(row.get("labels")),
            "assignees": parse_list(row.get("assignees")),
            "body": row.get("description"),
        }

        issue["labels"].append("imported-from-csv")

        try:
            result = r.create_issue(**issue)

        except Exception as e:
            fail += 1
            print(f"ERROR: {e}")
            continue

        success += 1
        print(result)

    print(f"***** Done! *****\n{success} issues created.\n{fail} issues failed.")


if __name__ == "__main__":
    main()
