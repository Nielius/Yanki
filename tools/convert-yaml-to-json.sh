#!/bin/bash
# This one-liner converts a yaml file into a json file using python.
#
# Probably would be better to just make this into a python script

python -c 'import sys, yaml, json; json.dump([x for x in yaml.load_all(sys.stdin)], sys.stdout, indent=4)' < perverse-sheaves.yml > perverse-sheaves.json
