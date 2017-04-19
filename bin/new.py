# File: new.py
#
# Command line tool to apply jinja2 template to
#
# Input: query & template

import argparse
import pymongo
import jinja2
import base64
import subprocess
import sys
# import IPython # for debugging purposes

parser = argparse.ArgumentParser()
parser.add_argument('--template', '-t',
                    help="use given file as a jinja2 template file",
                    default='answer-template.html')
parser.add_argument('--input', '-i',
                     help='A YAML file that contains questions, refs, answers.',
                     default='perverse-sheaves.yml')
parser.add_argument('--output', '-o',
                    help='the output .tex file',
                    default=False)
args = parser.parse_args()

inputfilename = args.input
outputfilename = args.output

# Jinja setup
# =======
# unfortunately, if you want to render a jinja template that is stored in a
# file, you need to go through a convoluted process of creating an
# "Environment" instance that contains the configuration. It can, for example,
# contain global variables that are available in all of the templates
jinjaEnv = jinja2.Environment(
    # this says that this jinja environment loads templates by looking for
    # files in the current directory
    loader=jinja2.FileSystemLoader('/home/niels/tmp/questionmaker/templates/'),
    autoescape=jinja2.select_autoescape(['htm', 'html', 'xml']))


# THE ACTUAL WORK
# ----------
client = pymongo.MongoClient()
db = client['testDB']
collection = db.perverseSheaves

if outputfilename:
  outputfile = open(outputfilename, 'w')
else:
  outputfile = sys.stdout

jinjatemplate = jinjaEnv.get_template(args.template)
outputfile.write(jinjatemplate.render(exclist=[x for x in collection.find()]))
