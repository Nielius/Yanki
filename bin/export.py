#!/usr/bin/env python
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

from qmutils import *
import convert

# Global constants

# Map a file extension to the corresponding pandoc filetype.
filetypeConversion = {
  'tex': 'latex'
}


# Small functions

def listTemplates():
  for templatepath in templateDirs:
    print("--- In {}:".format(templatepath))
    print('\n'.join([f for f in os.listdir(templatepath) if os.path.isfile(os.path.join(templatepath, f))]))
    print('\n')











def getOutputfileFromOptions(options):
  """Get a sensible default output filename and output filetype.

  If both filename and filetype are given,
  there is nothing to do.

  If only the filetype is given, use it to construct a sensible output filename
  from the input filename.

  If only the filename is given, extract the filetype from it.

  If none are given, assume the output filetype is HTML.
  """
  if ('output' in options) and ('filetype' in options):
    return options['output'], options['filetype']
  if options.get('output', '') != '': # i.e., exists and is not ''
    _, ext = os.path.splitext(options['output'])
    return options['output'], ext[1:]
  if options.get('filetype', '') != '':
    outputfilename = updatedFilename(inputfilename + '.out.' + options['filetype'])
    return outputfilename, options['filetype']
  else:
    return updatedFilename(options['input'] + '.out.html'), 'html'


def getTemplateFromOptions(options):
  """Use the options to find the template file.
  If a complete path to a template file is given, use it.
  Otherwise, search for the file in all template directories."""
  if not 'template' in options:
    raise NameError('No template given.')

  tf = options['template']

  for dir in ['./'] + list(options.get('templatedirs', [])):
    res = os.path.expanduser(os.path.join(dir, tf))
    if os.path.isfile(res):
      return res

  raise NameError('Template file not found.')



if __name__ == "__main__":
  # What are the options that we want to have?
  #
  # Put these things in dictionaries and merge them?
  # Or maybe only put flags in a dictionary?
  # Put defaults in the first dictionary and then have them overridden?
  #
  # Options that only make sense in the command line (and not in the config file):
  #
  # inputfilename --- file with source (yaml)
  # outputfilename --- file where output is stored; needs sensible default (in a function)
  #
  # Options that only make sense in the config file (and not on command line):
  #
  # templatedirs --- directories where template files are stored
  #
  # Options that make sense in both:
  #
  # noconvert (bool) --- do not convert strings from yaml to target
  # saveconverted (filename) --- save the pandoc converted string in the yaml file given by this option
  # debug (bool) --- display debugging information
  # outputfiletype (string) --- the file type (html, latex, ...) of the output; sensible default from outputfilename
  # template (str) --- template to be used to; if in config file, can be default template


  # Approach:
  #
  # The options from the config file and the command line options are both put in dictionaries
  # that are merged, where the command line files take priority.
  #
  # Important: for this merging to work, it is important that if an argument is
  # not given via the command line, its value should be `None`: otherwise, the
  # default argument from the command line would overwrite the argument from
  # the config file.


  # Parse command line arguments
  parser = argparse.ArgumentParser(description='''Script to apply a jinja2
  template to a yaml file describing a set of questions, possibly with answers
  and references.''')
  parser.add_argument('--config',
                      required=False,
                      help="use the given file as a config file")
  parser.add_argument('--template', '-t',
                      required=False,
                      help="use given file as a jinja2 template file; looks in different directories")
  parser.add_argument('--input', '-i',
                      required=True,
                      help='A YAML file that contains questions, refs, answers.')
  parser.add_argument('--output', '-o',
                      help='the output  file')
  parser.add_argument('--filetype', '-f',
                      required=False,
                      help='filetype of output (string)')
  parser.add_argument('--noconvert',
                      help='do not convert strings in yaml with pandoc; mostly for debugging purposes; useful in combination with the output from \'--saveconverted\'',
                      action='store_true')
  parser.add_argument('--saveconverted',
                      help='save the pandoc-converted yaml to this file')
  parser.add_argument('--debug',
                      help='display debugging information',
                      action='store_true')

  args = parser.parse_args()
  # Default options (overriden by config file, then by command line options)
  options = {'debug': False,
             'noconvert': False}

  # Read config files
  #
  configFiles = [os.path.expanduser(args.config)] if args.config \
    else [os.path.expanduser("~/.questionmaker.yaml")]

  for f in configFiles:
    if os.path.isfile(f):
      with open(f, 'r') as configFile:
        options.update(yaml.load(configFile))

  # Override config files with command line options and set some sensible defaults
  #
  options.update({k:v for k,v in vars(args).items() if v != None}) # TODO: fix this! this doesn't work yet, because vars(args) is a dictionary that contains all args; it will also have e.g. {'config': 'None'} if the user didn't give a config file

  inputfilename = options['input']
  outputfilename, outputfiletype = getOutputfileFromOptions(options)
  templateFilename = getTemplateFromOptions(options)

  if args.debug:
    print("Using the following options:")
    for name, value in options.items():
      print(name, value)


  # The main program now consists of the following three steps:
  #
  # 1. Import the yaml.
  # 2. Convert the markdown to the target filetype.
  # 3. Export using a template.

  # | - Main procedure: open yaml, convert and apply jinja template
  with open(inputfilename) as inputfile:
    # Import
    qs = yaml.load(inputfile)


    # Convert
    targetFiletype = filetypeConversion.get(outputfiletype, outputfiletype)
    for q in qs:
      q = convert.convertExercise(q, targetFiletype)


    # Export with Jinja
    # Jinja setup
    #
    # Unfortunately, if you want to render a jinja template that is stored in a
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
        # disabled_extensions=('htm', 'html', 'xml'))
    )


    if targetFiletype == 'latex':
        jinjaEnv = jinjaLatexEnv
    else:
        jinjaEnv = jinjaNormalEnv

    jinjatemplate = jinjaEnv.get_template(os.path.basename(templateFilename))
    with open(outputfilename, 'w') as outputfile:
      outputfile.write(jinjatemplate.render(exclist=qs))
