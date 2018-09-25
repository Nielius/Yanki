# File: new-md.py
#
# Description:
# This file takes a yaml-file and converts it into questions.
#
# Inner working:
# Load yaml file; apply pandoc to all strings in loaded file; apply jinja2 template.


# To include into a unit test (?):
# - if outputfilename is not given, choose reasonable standard
# - list templates in directories
# - does config file work as it is supposed to? does it indeed find one of the templates?

# TODO: does the saving the anki work properly? does the yaml file then contain references to the ids?

# TODO: option to list all available templates (use the function listTemplates)
# TODO: do not require the '-i' flag for the input file. (Just the positional argument.)



# Imports
import argparse
import os.path
import sys

import ruamel.yaml # see https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path if path incorrect
yaml = ruamel.yaml.YAML()
import jinja2

import pypandoc
# import IPython # for debugging purposes

from qmutils import *

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
                    required=False,
                    help="use given file as a jinja2 template file; looks in different directories",
                    default=False)
parser.add_argument('--input', '-i',
                    required=True,
                    help='A YAML file that contains questions, refs, answers.',
                    default='perverse-sheaves.yml')
parser.add_argument('--output', '-o',
                    required=False,
                    help='the output  file',
                    default='')
parser.add_argument('--anki', '-a',
                    help='save questions and answers to anki deck',
                    action='store_true')
parser.add_argument('--noconvert',
                    help='do not convert strings in yaml with pandoc; mostly for debugging purposes; useful in combination with the output from \'--saveconverted\'',
                    action='store_true')
parser.add_argument('--saveconverted',
                    help='save the pandoc-converted yaml to this file',
                    default=False)
parser.add_argument('--debug',
                    help='display debugging information',
                    action='store_true')
args = parser.parse_args()

templateDirs = [""] # where to look for templates
standardTemplate = os.path.expanduser("~/proj/questionmaker/templates/answer-clickable.html") # can be overridden by config file


# Read config file
configFiles = [os.path.expanduser("~/.questionmaker.yaml")]


try:
  configFilename = next(f for f in configFiles if os.path.isfile(f))
  with open(configFilename, 'r') as configFile:
    cfg = yaml.load(configFile)
    templateDirs.append(os.path.expanduser(cfg['templateDir']))
    standardTemplate = os.path.expanduser(cfg['standardTemplate'])
except StopIteration:
  print("No config file found.")
except:
  print("Unexpected error:", sys.exc_info()[0])
  raise


inputfilename = args.input
if args.output == '':
  _, ext = os.path.splitext(standardTemplate)
  outputfilename = updatedFilename(inputfilename + '.out' + ext)
else:
  outputfilename = args.output


# Get filename for the template
# 1. From args
# 2. From default in configuration file
# 3. From global default.
if args.template:
  templateFilename = args.template
else:
  templateFilename = standardTemplate

# Then: look for that file in the template directories
try:
  expandedTemplateFilenames = ( os.path.expanduser(d + templateFilename) for d in templateDirs )
  templateFilename = next(f for f in expandedTemplateFilenames if os.path.isfile(f))
except StopIteration:
  print("No template file found.")


if args.debug:
  print("Using the following options:")
  for name, value in globals().copy().items():
    print(name, value)




def listTemplates():
  for templatepath in templateDirs:
    print("--- In {}:".format(templatepath))
    print('\n'.join([f for f in os.listdir(templatepath) if os.path.isfile(os.path.join(templatepath, f))]))
    print('\n')



 
# Jinja setup
# unfortunately, if you want to render a jinja template that is stored in a
# file, you need to go through a convoluted process of creating an
# "Environment" instance that contains the configuration. It can, for example,
# contain global variables that are available in all of the templates
jinjaLatexEnv = jinja2.Environment(
    # this says that this jinja environment loads templates by looking for
    # files in the current directory
    loader=jinja2.FileSystemLoader(os.path.dirname(templateFilename)),
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
    loader=jinja2.FileSystemLoader(os.path.dirname(templateFilename)),
    # autoescape=jinja2.select_autoescape(
    #   disabled_extensions=('htm', 'html', 'xml'))
)



# |- Convert markdown string to some target file type with pandoc
def convertMarkdownFn(x: str, targetft: str) -> str:
  return pypandoc.convert_text(x, targetft, format='md')
# As a one-liner: convertMarkdownFn = (lambda x: pypandoc.convert_text(x, targetFiletype, format='md'))

def convertQuestion(q, targetft):
  """Convert the fields of a question (a dictionary with lots of fields) to the target file type targetft using pandoc.
  Essentially, this is  just some kind of mapcar over a dictionary."""
  return {k: (convertMarkdownFn(v, targetft) if isinstance(v, str) else v) for k, v in q.items()}


def convertAllQuestions(qs, targetft):
  "Convert all strings in the yaml doc qs from markdown to targetft."
  # Depends on the following global variables, that correspond to command line options.
  # - args.noconvert
  # - args.saveconverted
  if args.noconvert: # this is a command-line option that disables converting
    qsconv = qs
  else:
    qsconv = map((lambda x : convertQuestion(x, targetft)), qs) # the converted questions

  # Save the converted strings if that option is given
  if args.saveconverted:
    with open(args.saveconverted, "w") as convertedoutfile:
      convertedoutfile.write(yaml.dump([x for x in qsconv]))

  return qsconv


# | - Main procedure: open yaml, convert and apply jinja template
with open(inputfilename) as inputfile:
  qs = yaml.load(inputfile) # the questions; should return a generator
                                # (sort of list?) of dictionaries

  # OPTION 1: Apply Jinja2 template
  if outputfilename: # if an outputfilename was given as an option: convert, apply template and save
    with open(outputfilename, 'w') as outputfile:

      # Get the target extension from the outputfilename.
      _, targetFiletype = os.path.splitext(outputfilename) # get the extension of # the outputfilename; # this is target file # type
      targetFiletype = targetFiletype[1:] # remove the dot at the beginning
      # sometimes the extension is not the same as the target name that pandoc uses; change in that case:
      if targetFiletype in filetypeConversion.keys():
        targetFiletype = filetypeConversion[targetFiletype]

      qsconv = convertAllQuestions(qs, targetFiletype)

      if targetFiletype == 'latex':
        jinjaEnv = jinjaLatexEnv
      else:
        jinjaEnv = jinjaNormalEnv

      # Apply the jinja template.
      jinjatemplate = jinjaEnv.get_template(os.path.basename(templateFilename))
      outputfile.write(jinjatemplate.render(exclist=qsconv))

# OPTION 2: Save files to anki
if args.anki:
  import sys
  sys.path.append("/home/niels/proj/anki") # this should probably not really be part of the code
  from anki.storage import Collection
  profileHome = "/home/niels/.local/share/Anki2/Tmpuser"
  collectionPath = os.path.join(profileHome, 'collection.anki2')
  col = Collection(collectionPath, log=True)
  col.conf['curModel'] = 1 # this is just the basic model with only a question and an answer

  qsconv = convertAllQuestions(qs, 'html')

  # Now add all the questions as notes
  for q in qsconv:
    note = col.newNote()
    note.fields[0] = q.get('question', '') # the second is the default value if key 'question' doesn't exist
    note.fields[1] = q.get('answer', '') # i.d.
    col.addNote(note)

  col.save()
