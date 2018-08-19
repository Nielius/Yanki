# File: new-md.py
#
# Description:
# This file takes a yaml-file and converts it into questions.
#
# Inner working:
# Load yaml file; apply pandoc to all strings in loaded file; apply jinja2 template.

# Imports
import argparse
import os.path

import yaml
import jinja2

import pypandoc
# import IPython # for debugging purposes


# Global constants

# Map a file extension to the corresponding pandoc filetype.
filetypeConversion = {
  'tex': 'latex'
}


# Parsing the arguments
parser = argparse.ArgumentParser(description='''Script to apply a jinja2
template to a yaml file describing a set of questions, possibly with answers
and references.''')
parser.add_argument('--template', '-t',
                    required=True,
                    help="use given file as a jinja2 template file",
                    default='latex-template.tex')
parser.add_argument('--input', '-i',
                    required=True,
                    help='A YAML file that contains questions, refs, answers.',
                    default='perverse-sheaves.yml')
parser.add_argument('--output', '-o',
                    required=True,
                    help='the output .tex file',
                    default='questions.tex')
parser.add_argument('--noconvert',
                    help='do not convert strings in yaml with pandoc; mostly for debugging purposes',
                    action='store_true')
parser.add_argument('--saveconverted',
                    help='save the pandoc-converted yaml to file',
                    default=False)
args = parser.parse_args()

inputfilename = args.input
outputfilename = args.output

# Get the target extension from the outputfilename.
_, targetFiletype = os.path.splitext(outputfilename) # get the extension of # the outputfilename; # this is target file # type
targetFiletype = targetFiletype[1:] # remove the dot at the beginning
# sometimes the extension is not the same as the target name that pandoc uses; change in that case:
if targetFiletype in filetypeConversion.keys():
  targetFiletype = filetypeConversion[targetFiletype]


 
# Jinja setup
# unfortunately, if you want to render a jinja template that is stored in a
# file, you need to go through a convoluted process of creating an
# "Environment" instance that contains the configuration. It can, for example,
# contain global variables that are available in all of the templates
jinjaLatexEnv = jinja2.Environment(
    # this says that this jinja environment loads templates by looking for
    # files in the current directory
    loader=jinja2.FileSystemLoader('../templates'),
    # Change the default delimiters used by Jinja such that it won't pick up
    # brackets attached to LaTeX macros. Stolen from
    # http://tex.stackexchange.com/questions/40720/latex-in-industry
    block_start_string = '%{',
    block_end_string = '%}',
    comment_start_string = '%{#',
    comment_end_string = '%#}',
    variable_start_string = '%{{',
    variable_end_string = '%}}',
    autoescape=jinja2.select_autoescape(['htm', 'html', 'xml']))

jinjaNormalEnv = jinja2.Environment(
    # this says that this jinja environment loads templates by looking for
    # files in the current directory
    loader=jinja2.FileSystemLoader('../templates'),
    # autoescape=jinja2.select_autoescape(
    #   disabled_extensions=('htm', 'html', 'xml'))
)

if targetFiletype == 'latex':
  jinjaEnv = jinjaLatexEnv
else:
  jinjaEnv = jinjaNormalEnv


# |- Convert markdown string to some target file type with pandoc
def convertMarkdownFn(x: str, targetft: str) -> str:
  return pypandoc.convert_text(x, targetft, format='md')
# As a one-liner: convertMarkdownFn = (lambda x: pypandoc.convert_text(x, targetFiletype, format='md'))



# | - Main procedure: open yaml, convert and apply jinja template
with open(inputfilename) as inputfile, \
     open(outputfilename, 'w') as outputfile:
  qs = yaml.load(inputfile) # the questions; should return a generator
                                # (sort of list?) of dictionaries


  # Convert all the strings from markdown to the right target.
  # | - The converted questions (i.e., convert the strings in the yaml document
  # | - with pandoc to the targetFiletype)
  if args.noconvert: # this is a command-line option that disables converting
    qsconv = qs
  else:
    qsconv = map(
      (lambda x : {k: (convertMarkdownFn(v, targetFiletype) if isinstance(v, str) else v)
                   for k, v in x.items()} ),
      qs) # the converted questions

  # Save the converted strings if that option is given
  if args.saveconverted:
    with open(args.saveconverted, "w") as convertedoutfile:
      convertedoutfile.write(yaml.dump([x for x in qsconv]))


  # Apply the jinja template.
  jinjatemplate = jinjaEnv.get_template(args.template)
  outputfile.write(jinjatemplate.render(exclist=qsconv))
