# File: new.py
#
# Command line tool to apply jinja2 template to a set of questions.
# The difference between this script and the script main.py is that this script
# uses a MongoDB as a back-end, instead of a yaml file.
#
# Input: query & template

import argparse
import pymongo
import jinja2
from orgConverter import orgConvert
from dictlistmap import dictlistmap
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
    loader=jinja2.FileSystemLoader('/home/niels/tmp/questionmaker/templates/')
    # autoescape=jinja2.select_autoescape(['htm', 'html', 'xml'])
)


# THE ACTUAL WORK
# ----------
client = pymongo.MongoClient()
db = client['testDB']
collection = db.perverseSheaves

if outputfilename:
  outputfile = open(outputfilename, 'w')
else:
  outputfile = sys.stdout

orgConvertFn = (lambda x: orgConvert(x, 'html'))

jinjatemplate = jinjaEnv.get_template(args.template)
outputfile.write(jinjatemplate.render(exclist=[dictlistmap(orgConvertFn, x) for x in collection.find()]))

# je kunt zoiets ook redelijk makkelijk handmatig doen:
# # import pymongo
# from pymongo import MongoClient
# client = MongoClient('localhost', 27017)

# db = client['bibtex'].entries

# for i, result in enumerate(db.find({"year" : {"$lt": "1950"}})):
#     print('{i: 2d}. {author}, {title}, {journal}, {year}.'.format(i=i+1, **result))
