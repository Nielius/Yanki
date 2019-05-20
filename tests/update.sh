#!/bin/bash
# The tests should be reproducible
# and also: everything should be automatic.

cd "$(dirname "${BASH_SOURCE[0]}")"
. variables.sh

for file in "${arrayoftestfiles[@]}"; do
    echo "Sending ${file} to ${ankicollection}".
    yanki a -c "${ankicollection}" "${file}"
    echo -e "Done.\n\n"
done

# Start Anki with Testuser as profile
anki -p Testuser &


echo "$(date -Iminutes): updated Anki." >> log
