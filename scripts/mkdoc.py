import glob
import itertools
import json

for profile in glob.glob("profiles/*.json"):
    profileid = profile[9:-5]
    with open(profile) as f:
        profilemeta = json.load(f)
        with open(f"profiles/{profileid}.md", "w") as clf:
            print("# Included patches", file=clf)
            for patch in itertools.chain(*[sorted(glob.glob(f"patches/{patch}.json")) for patch in profilemeta["patches"]]):
                patchid = patch[8:-5]
                with open(patch) as f:
                    patchmeta = json.load(f)
                    if "changelog" in patchmeta and "pr_number" in patchmeta:
                        cl = patchmeta["changelog"]
                        pr = patchmeta["pr_number"]
                        print(file=clf)
                        print(f"By {cl['author']} in [#{pr}](https://github.com/space-wizards/space-station-14/pull/{pr}):", file=clf)
                        for entry in cl["changes"]:
                            print(f"- {entry['type'].lower()}: {entry['message']}", file=clf)
