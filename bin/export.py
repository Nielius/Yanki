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
