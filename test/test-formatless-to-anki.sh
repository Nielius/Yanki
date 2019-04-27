#!/bin/bash
# cp formatless-test-file.md.bak formatless-test-file.md
python ../bin/yanki.py a \
       -d testdeck \
       -c /home/niels/.local/share/Anki2/Testuser/collection.anki2 \
       formatless-test-file.md
