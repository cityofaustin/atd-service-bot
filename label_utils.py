"""
Utilities for managing github labels.
"""
import requests
from config.secrets import GITHUB_USER, GITHUB_PASSWORD

    
def get_all_labels(repo_name):
    """ get all labels from `repo_name` """
    labels = []

    url = f"https://api.github.com/repos/cityofaustin/{repo_name}/labels"

    last_url = None

    while True:

        res = requests.get(url, params={"per_page":100}, auth=(GITHUB_USER, GITHUB_PASSWORD))
        
        res.raise_for_status()
    
        for label in res.json():
            labels.append(label)

        if url == last_url:
            break

        try:
            links = requests.utils.parse_header_links(res.headers["Link"])
        except KeyError:
            # if there's only one page there will be no link headers
            break

        if links:
            for link in links:
                if link.get("rel") == "next":
                    url = link.get("url")
                    print(url)
                elif link.get("rel") == "last":
                    last_url = link.get("url")

        return labels


def update_label(repo_name, label_name, new_label):
    """
    Update a label given a `repo_name` str, existing `label_name` str, and `new_label` dict.

    The `new_label` dict should be structured like so (each field is optional):
    
    {
        "new_name": "bug :bug:",
        "description": "Small bug fix required",
        "color": "b01f26"
    }
    
    See: https://developer.github.com/v3/issues/labels/#update-a-label
    """
    url = f"https://api.github.com/repos/cityofaustin/{repo_name}/labels/{label_name}"

    res = requests.patch(url, json=new_label, auth=(GITHUB_USER, GITHUB_PASSWORD))

    res.raise_for_status()
    return res
