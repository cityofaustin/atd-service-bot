import pdb
from pprint import pprint as print

import knackpy
import requests

from config.config import *
from config.secrets import API_KEY, GITHUB_USER, GITHUB_PASSWORD
from transforms import *


# get issue notes that have not been migrated

kn = knackpy.Knack(
    scene="scene_127",
    view="view_245",
    app_id=KNACK_APP["app_id"],
    api_key=API_KEY,
    ref_obj=["object_7"],
)

for note in kn.data:
    comment = note["Note"]
    created_by = note["Created by"]
    created_date = mills_to_timestamp(note["Created Date"])
    comment = f"{comment}\n\nCreated By: {created_by}\nCreated Date: {created_date}"
    issue_number = note["Github Issue Number"]
    repo = note["Repo Name"]
    
    endpoint = f"https://api.github.com/repos/cityofaustin/{repo}/issues/{issue_number}/comments"
    
    res = requests.post(endpoint, json={"body" : comment}, auth=(GITHUB_USER, GITHUB_PASSWORD))

    res.raise_for_status()

    knack_id = note["id"]

    url = res.json()["html_url"]

    knack_record_update = {
        "id": knack_id,
        "field_372": "Successful",  # github note migration result
        "field_377" : url
    }

    res = knackpy.record(
        knack_record_update,
        obj_key="object_7",
        app_id=KNACK_APP["app_id"],
        api_key=API_KEY,
        method="update",
    )

    print(issue_number)
    print(comment)