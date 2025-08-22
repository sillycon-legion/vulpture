import glob
import json

print("# Included patches")
for patch in glob.glob("patches/*.json"):
    patchid = patch[8:-5]
    with open(patch) as f:
        patchmeta = json.load(f)
        if "changelog" in patchmeta and "pr_number" in patchmeta:
            cl = patchmeta["changelog"]
            pr = patchmeta["pr_number"]
            print()
            print(f"By {cl['author']} in [#{pr}](https://github.com/space-wizards/space-station-14/pull/{pr}):")
            for entry in cl["changes"]:
                print(f"- {entry['type'].lower()}: {entry['message']}")
