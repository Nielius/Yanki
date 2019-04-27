#!/bin/bash

python ../bin/yanki.py e  -f html formatless-test-file.md output.html
firefox output.html &
