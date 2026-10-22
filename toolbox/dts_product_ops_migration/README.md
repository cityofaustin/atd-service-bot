The scripts in this directory were used in service of the Project: Implement GitHub Projects Product Ops [29157](https://github.com/cityofaustin/atd-data-tech/issues/29157). The scripts are idempotent unless otherwise stated. 

We historically used issue labels to categorize and tag our work. In February of 2026 we started using GithubProject boards. However now that [Issue Fields](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-and-managing-issue-fields) are available, we will are migrating our information from labels and project fields to issue fields.

https://github.com/cityofaustin/atd-data-tech/issues/28739

In order to enable issue fields for the majority of our issues, the issues need to be of type "Task". `update_issue_task.py` queries all issues that lack a type from our repo and assigns the type "Task". 

We now have the policy that each task can only have one team assigned.  `update_team_label.py` queries all issues from our repo that match the team label (ex: "Team: Dev"), checks that no other teams are also assigned to the same issue, and then sets the DTS Team issue field to the correct team (ex: "Dev") as long as there is no existing DTS Team assigned. Repeat the script per team. 

`update_teams_label.py` (note the _s_) adds Teams to Epic's DTS Teams field. This field is a multiselect whereas the Team label is single select. 

`update_divisions_field.py` updates the Divisions issue field based on Workgroups labels.

https://github.com/cityofaustin/atd-data-tech/issues/29765

Some of the issue fields (estimates and status) are populated from information on individual project boards. `estimates_status.py` queries a project board and updates the estimate and status issue field. If an issue's issue field is already populated, the script does not make any changes.



