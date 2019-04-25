#!/usr/bin/env python
#
# This is the CLI.

import argparse
import sys

import export
import convert

from formatless import FormatlessToNotesCollection, NotesCollectionToFormatless
from yamlinterface import YAMLToNotesCollection, NotesCollectionToYAML

def NotesCollectionFunctionsFromFile(filename):
    """Returns two functions: the first to import a NotesCollection from a file
    of the same filetype as the argument filename, and the second to export a NotesCollection
    to such a file.

    The import function expects as input a file handler for reading.
    The output function expects as input a NotesCollection and a file handler for writing.
    """
    if filename.endswith('.md'):
        return FormatlessToNotesCollection, NotesCollectionToFormatless
    elif filename.endswith('.yml') or filename.endswith('.yaml'):
        return YAMLToNotesCollection, NotesCollectionToYAML
    else:
        raise ValueError(f'No known import/export functions for file {filename}.')


class Yanki(object):
    """This allows us to use argparse with several subcommands,
    as in for example git.

    The idea of the code was taken from
    https://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
    """

    def __init__(self):
        # Allow the following abbreviations for frequently used commands:
        self.a = self.ankify
        self.y = self.yamlify
        self.e = self.export

        # Initialize main parser
        parser = argparse.ArgumentParser(
            description='Export flashcards to Anki or jinja2 templating system.',
            usage='''yanki <command> [<args>]

The supported commands are
   a(nkify)    Save a file in an anki collection
   e(xport)    Export an exercise file using a jinja2 template
   y(amlify)   Turn a formatpoor markdown file into a yaml file
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def ankify(self):
        parser = argparse.ArgumentParser(
            description='Add the yanki cards to an anki collection. Accepts yaml files and markdown files following the "formatless" syntax.')
        parser.add_argument('infile', nargs='?', type=argparse.FileType('r+'),
                            default=sys.stdin)
        parser.add_argument('--collection', '-c',
                            required=False,
                            help="use this collection instead of the collection in the metadata")
        parser.add_argument('--deck', '-d',
                            required=False,
                            help='use this deck instead of the deck in the metadata')
        parser.add_argument('--noupdate', '-n',
                            action='store_true',
                            help='do not update the input file with anki ids')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (yanki) and the subcommand (ankify)
        args = parser.parse_args(sys.argv[2:])

        # The actual Anki update
        ncimport, ncexport = NotesCollectionFunctionsFromFile(args.infile.name)
        ncol = ncimport(args.infile)
        ncol.writeToAnki(deck = args.deck,
                         collection = args.collection)
        if args.noupdate is not True:
            ncexport(ncol, args.infile)



    def export(self):
        """Export a yanki file to some other file format, using a jinja2 template."""
        # Parse the arguments.
        # This is only the first step; most of the work is done in export.mergeArgsWithDefaults.
        # For this reason, I do not have any defaults here.
        # (Argumens not given on the command line should have the value 'None'.)
        parser = argparse.ArgumentParser(
            description='Export a markdown or yaml file with exercises to some other file using a jinja2 template.')
        parser.add_argument('infile', # nargs='?',
                            type=argparse.FileType('r'),
                            default=sys.stdin)
        parser.add_argument('outfile', # nargs='?',
                            type=argparse.FileType('w'),
                            default=sys.stdout)
        parser.add_argument('--template', '-t',
                            required=False,
                            help="use this as a jinja2 template")
        parser.add_argument('--filetype', '-f',
                            required=False,
                            help='filetype of output (string)')
        parser.add_argument('--config',
                            required=False,
                            help="use the given file as a config file")
        parser.add_argument('--noconvert',
                            required=False,
                            help="do not convert the text in the yaml files (UNIMPLEMENTED)")
        parser.add_argument('--saveconverted',
                            required=False,
                            help="save the converted text in another yaml file (UNIMPLEMENTED)")
        parser.add_argument('--debug',
                            required=False,
                            help="display extra debugging information (partially implemented)")

        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (yanki) and the subcommand (ankify)
        args = parser.parse_args(sys.argv[2:])

        options = export.mergeArgsWithDefaults(args)

        # Get all the questions as a list of dictionaries
        ncimport, ncexport = NotesCollectionFunctionsFromFile(args.infile.name)
        ncol = ncimport(args.infile)
        qs = ncol.notes

        # Convert
        targetFiletype = options['targetFiletype']
        for q in qs:
            q = convert.convertExercise(q, targetFiletype)

        export.jinjaExport(
            qs,
            options['templateFilename'],
            options['outfile'],
            options['targetFiletype'])

        print('Running export.')

    def yamlify(self):
        parser = argparse.ArgumentParser(
            description='Turn a formatpoor markdown file into a yaml file.')
        parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                            default=sys.stdin)
        parserer.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                            default=sys.stdout)


if __name__ == '__main__':
    Yanki()
