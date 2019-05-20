#!/bin/bash
# This backs up the current Yanki files in this folder
# and backs up the current state of the Anki database.

cd "$(dirname "${BASH_SOURCE[0]}")"
. variables.sh


# 1. Backing up Anki collection
echo "Backing up Anki collection ${ankicollection} to ${backupcollection}."
cp -v "${ankicollection}" "${backupcollection}"
echo "Done."

# 2. Back up all the Yanki files
echo "Copying:"
for file in "${arrayoftestfiles[@]}"; do
    cp -v "${file}" ${file}.bak
done


echo "$(date -Iminutes): backed up." >> log
