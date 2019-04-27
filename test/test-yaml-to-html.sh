#!/bin/bash
# cp formatless-test-file.md.bak formatless-test-file.md
python ../bin/yanki.py e -f html bash-yanki.yml output.html
firefox output.html &
