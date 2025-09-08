import requests
import os
import glob
import json

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]

for patch in glob.glob("patches/**/*.json", recursive=True):
    patchid = patch[8:-5]
    with open(patch) as f:
        patchmeta = json.load(f)
        if "pr_number" in patchmeta and "commit" in patchmeta:
            pr = requests.get(f"https://api.github.com/repos/space-wizards/space-station-14/pulls/{patchmeta['pr_number']}", headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Authorization": f"Bearer {GITHUB_TOKEN}"
            }).json()
            if pr["merged"]:
                print(f"{patch} is merged, should be deleted")
            if pr["head"]["sha"] != patchmeta["commit"]:
                print(f"{patch} commits are different from patch: patch {patchmeta['commit']}, PR {pr['head']['sha']}")
        elif "repo" in patchmeta and "branch" in patchmeta and "commit" in patchmeta:
            branch = requests.get(f"https://api.github.com/repos/{patchmeta['repo']}/branches/{patchmeta['branch']}", headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Authorization": f"Bearer {GITHUB_TOKEN}"
            }).json()
            if branch["commit"]["sha"] != patchmeta["commit"]:
                print(f"{patch} commits are different from patch: patch {patchmeta['commit']}, PR {branch['commit']['sha']}")
