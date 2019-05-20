#!/bin/bash
# Restore everything to its prior state:
#
# 1. Reset Anki database to its old version.
# 2. Remove all buddy files (yanki.md.yml files).
# 3. Delete all metadata in the yanki files by copying over the yanki.md.bak files.

# 0. Import variables that specify where the Anki collection and its backup are.
cd "$(dirname "${BASH_SOURCE[0]}")"
. variables.sh

echo "Restoring Anki database."
cp -v "${backupcollection}" "${ankicollection}"


echo "Removing buddy files."
rm -v *yanki.md.yml


echo "Restoring backed up Yanki files."
for file in *yanki.md.bak; do
    cp -v "${file}" "${file%.bak}"
done

echo "$(date -Iminutes): restored backup." >> log
