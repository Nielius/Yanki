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

from configfile import globalConfig


# Global constants

# Map a file extension to the corresponding pandoc filetype.
filetypeConversion = {
  'tex': 'latex'
}





def getOutputfileFromOptions(options):
  """Get a sensible default output filename and output filetype.
  At the moment, we do not use this function.

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

def getOutputfileFormat(outfile, templateFilename):
  """Deduce the output filetype from the outputfile or filename of the template.
  Tries to use the extension of the outfile first;
  then considers the templateFilename (for example if std.out is the output).
  """
  # First attempt
  res = os.path.splitext(outfile.name)[1][1:]
  if res != '':
    return res

  # Second attempt
  res = os.path.splitext(templateFilename)[1][1:]
  if res != '':
    return res

  raise NameError('Cannot find appropriate output filetype!')



def getTemplateFromOptions(templateFilename, templateDirs):
  """Use the options to find the template file.
  If a complete path to a template file is given, use it.
  Otherwise, search for the file in all template directories."""

  if templateFilename is None:
    raise ValueError('No template filename given!')

  for dir in [''] + templateDirs:
    res = os.path.expanduser(os.path.join(dir, templateFilename))
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
    else []

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




def jinjaExport(exclist, templateFilename, outfile, targetFiletype=None):
  """Export the exclist according to the jinja template stored in templateFilename.
  Save the result in outfile (a stream).

  If target filetype is not given, deduce it from templateFilename.
  """
  if targetFiletype == None:
    targetFiletype = os.path.splitext(templateFilename)[1][1:]

  # Export with Jinja
  # Jinja setup
  #
  # Unfortunately, if you want to render a jinja template that is stored in a
  # file, you need to go through a convoluted process of creating an
  # "Environment" instance that contains the configuration. It can, for example,
  # contain global variables that are available in all of the templates
  if targetFiletype == 'latex':
    jinjaEnv = jinja2.Environment(
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

  else:
    jinjaEnv = jinja2.Environment(
      # this says that this jinja environment loads templates by looking for
      # files in the current directory
        loader=jinja2.FileSystemLoader(os.path.dirname(templateFilename)),
      # autoescape=jinja2.select_autoescape(
      # disabled_extensions=('htm', 'html', 'xml'))
      )


  jinjatemplate = jinjaEnv.get_template(os.path.basename(templateFilename))
  outfile.write(jinjatemplate.render(exclist=exclist, title=os.path.basename(outfile.name)))




def mergeArgsWithDefaults(args):
  """Merge the arguments obtained form argparse with the defaults contained in the configuration file.
  The command line options take priority.

  Returns a dictionary of the following options:

  - infile: file --- the input file
  - outfile: file --- the output file
  - templateFilename: str --- the filename of the template
  - targetFiletype: str --- the filetype of the target; deduced from the filename of the output file or the template filename, unless explicitely given
  - noconvert: bool --- if true, do not convert the yaml input
  - debug: bool --- display debugging information

  Note that the configuration files can have an option 'templateDirs',
  which specifies the directories in which to look for templates.
  """

  # Structure of this code:
  # 1. Set defaultOptions (dict of default options).
  # 2. Set configOptions (dict of options from config files).
  # 3. Set cliOptions (dict of options from command line interface).
  # 4. Merge these options (using conservativeDictUpdate).
  # 5. Fill in any gaps using sensible defaults (such as targetFiletype, which
  #    can be deduced from the name of the template or the output filename.)

  # Default options (overriden by config file, then by command line options).
  # This is what we will return.
  defaultOptions = {
    'infile': None, # no default
    'outfile': None, # no default
    'templateFilename': None, # no default
    'targetFiletype': None, # set default below
    'debug': False,
    'noconvert': False}


  # Read config files
  configOptions = {}
  configFiles = [os.path.expanduser(args.config)] if args.config \
    else []

  for f in configFiles:
    if os.path.isfile(f):
      with open(f, 'r') as configFile:
        configOptions.update(yaml.load(configFile))

  # An alias in the config options: use 'template' instead of 'templateFilename'
  configOptions['templateFilename'] = configOptions.get('template', None)


  # Options from command line interface
  cliOptions = {
    'infile': args.infile,
    'outfile': args.outfile,
    'templateFilename': args.template,
    'targetFiletype': args.filetype,
    'debug': args.debug,
    'noconvert': args.noconvert
  }


  # Merge
  options = defaultOptions # will return this
  conservativeDictUpdate(options, configOptions)
  conservativeDictUpdate(options, cliOptions)


  # Deduce sensible defaults

  # Search for the template

  templateDirs = ['./']
  globalconfig = globalConfig()

  templateDirs.extend(globalconfig.get('templateDirs') or [])

  # Some other defaults:
  templateDirs.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../templates/'))

  options['templateFilename'] = getTemplateFromOptions(
      options['templateFilename'],
      templateDirs + list(configOptions.get('templateDirs', [])))


  # Deduce the target filetype, if it hasn't been given yet.
  if options['targetFiletype'] is None:
    options['targetFiletype'] = getOutputfileFormat(options['outfile'], options['templateFilename'])



  if args.debug:
    print("Using the following options:")
    for name, value in options.items():
      print(name, value)

  return options


def conservativeDictUpdate(x, y):
  """Update dictionary x with dictionary y, but conservatively:
  do not create any new keys in x
  and if a value in y is `None`, then do not update that value.
  """
  for key, value in x.items():
    if y.get(key) is not None:
      x[key] = y[key]
