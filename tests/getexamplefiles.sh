#!/bin/bash
# copy all example files from my doc dir and remove metadata from them

scriptdir="$( cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd )"
echo $scriptdir
find ~/doc/ -iname "*yanki.md" -type f -execdir cp -t $scriptdir {} +

# Delete all metadata lines:
for file in *yanki.md; do
    sed -i '/^uuid /d' "${file}"
    sed -i '/^anki-guid /d' "${file}"
done


