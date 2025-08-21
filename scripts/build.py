import subprocess
import glob
import shutil
import os
import json
import publish_multi_request

if os.path.isdir("src"):
    shutil.rmtree("src")
if os.path.isdir("release"):
    shutil.rmtree("release")

subprocess.run(["git", "clone", "--recursive", "--depth", "1", "https://github.com/space-wizards/space-station-14.git", "src"], check=True)

def get_engine_version() -> str:
    proc = subprocess.run(["git", "describe", "--tags", "--abbrev=0"], stdout=subprocess.PIPE, cwd="src/RobustToolbox", check=True, encoding="UTF-8")
    tag = proc.stdout.strip()
    assert tag.startswith("v")
    return tag[1:] # Cut off v prefix.

def get_ss14_version() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, cwd="src", check=True, encoding="UTF-8")
    tag = proc.stdout.strip()
    return tag

def get_vulpture_version() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, check=True, encoding="UTF-8")
    tag = proc.stdout.strip()
    return tag

def get_version() -> str:
    return get_vulpture_version() + "-orig-" + get_ss14_version()

for patch in glob.glob("patches/*.json"):
    patchid = patch[8:-5]
    with open(patch) as f:
        patchmeta = json.load(f)
        if "changelog" in patchmeta:
            with open(f"src/Resources/Changelog/Parts/{patchid}.yml", "w") as cl:
                json.dump(patchmeta["changelog"], cl)
        subprocess.run(["git", "apply", f"../patches/{patchid}.patch"], cwd="src", check=True)
        print(f"applied patch {patchid}")

subprocess.run(["dotnet", "restore"], cwd="src", check=True)
subprocess.run(["dotnet", "build", "Content.Packaging", "--configuration", "Release", "--no-restore", "/m"], cwd="src", check=True)
# subprocess.run(["dotnet", "run", "--project", "Content.Packaging", "server", "--hybrid-acz", "--platform", "linux-x64"], cwd="src", check=True)
subprocess.run(["dotnet", "run", "--project", "Content.Packaging", "server", "--platform", "win-x64", "--platform", "linux-x64", "--platform", "osx-x64", "--platform", "linux-arm64"], cwd="src", check=True)
subprocess.run(["dotnet", "run", "--project", "Content.Packaging", "client", "--no-wipe-release"], cwd="src", check=True)
shutil.move("src/release", "release")

publish_multi_request.publish(get_version(), get_engine_version())
shutil.rmtree("src")