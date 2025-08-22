#!/usr/bin/env bash
cd ../space-station-14
git diff --binary $(git merge-base master $1) $1 > ../vulpture/patches/$2.patch
cat > ../vulpture/patches/$2.json << EOF
{
    "pr_number": $2,
    "commit": "$(git rev-parse $1)",
    "changelog": {
        "author": "TODO",
        "changes": [
            {
                "type": "Add",
                "message": "TODO"
            }
        ]
    }
}
EOF