# formatless.py
#
# Reads and writes so-called "formatless" files.
#
# For read: `Formatless.__init__(self, filename)`.
# For write: `writeListToFormatless(data, outfile)`.
#
#
# Intro
#
# "Formatless" is a file syntax that is not so expressive, but expressive
# enough for basic yanki cards. The main advantage is that it is simply a
# markdown file in a specific format (the first sentence of every paragraph is
# the question; the rest is the answer; possibly this paragraph is preceded by
# some metadata) that can very easily and quickly be read and written by a
# human, using any text editor. It is much less of a hassle to read and write
# than comparable YAML files.
#
# A possible (as of yet only partially implemented) extension would be to have
# a formatless file together with a metadata file. This metadata file could be
# more complicated (e.g. YAML or sexps) and use the IDs of the cards in
# formatless to express more difficult relations (such as hierarchies of the
# notes, or general metadata).
#
#
# Informal specification of the syntax:
#
# 1. Questions are separated by newlines (except for newlines within code
# blocks).
#
# 2. The first line that does not start with 'id ', 'uuid ' or 'anki-guid ' is the question. The
# question is always only one line.
#
# 3. Everything that follows the question, is the answer.
#
# 4. Questions may optionally start with 'id [id]' (or similarly for 'uuid' and 'anki-guid') to denote the id.
#
# 5. There are no escape sequences. The only special situation is markdown code
# blocks, which start with '```' on a line and end with a line that is only
# '````.
#
#
# Usage:
#
# - `Formatless.__init__(self, filename)`: open and parse a file with formatless syntax
# - `Formatless.writeToFile(self, filename)`: write the data to a formatless file
# - `writeListToFormatless(data, outfile)`: write any list of question, answer and id to outfile in formatless syntax

from enum import Enum
from notescollection import NotesCollection, NotesCollectionMetadata
import yaml
import os.path
from os import environ
from uuid import uuid4 as uuid
from base32helpers import b32stren, b32strde

# To track the state of the parser:
pstate = Enum('Parser state',
              'preamble ' + # ids and probably other metadata of the function
              'question ' + # reading the question
              'answer ' + # reading the answer
              'outside') # not reading a question

def writeListToFormatless(data, outfile):
    """Writes data (a list of dictionaries (with (optionally) id, question,
    answer)) to outfile as a formatless file.

    """
    outfile.seek(0)
    for exc in data:
        if 'uuid' not in exc:
            exc['uuid'] = str(uuid())
        outfile.write('uuid ' + str(exc['uuid']) + '\n')
        if 'id' in exc:
            outfile.write('id ' + str(exc['id']) + '\n')
        if 'anki-guid' in exc:
            outfile.write('anki-guid ' + b32stren(exc['anki-guid']) + '\n')
        if 'question' in exc:
            outfile.write(exc['question'] + '\n')
        else:
            raise ValueError('This exercise does not have a question!')
        if 'answer' in exc:
            outfile.write(exc['answer'] + '\n')
        outfile.write('\n')

def NotesCollectionToFormatless(col, outfile):
    """Writes the data of a NotesCollection to the file outfile.
    (This outfile is not a string, but a file object.)
    The metadata is written to outfile.name + '.yml' by default."""
    with open(outfile.absolutepath + '.yml', 'w') as metaoutfile:
        print(f'Writing to {os.path.realpath(metaoutfile.name)}.')
        try:
            writeListToFormatless(col.notes, outfile)
            yaml.dump(col.metadata.asDict(), metaoutfile)

        except yaml.YAMLError as exc:
            print(exc)

def FormatlessToNotesCollection(filename):
    return Formatless(filename).asNotesCollection()


class Formatless:
    """Parses formatless files."""

    def __init__(self, infile):
        """Initializes a file with formatless syntax: opens the file, parses it, and
        stores the resulting list of dictionaries (with question, answer and
        possibly id) in `self.data`.
        """
        self.file = infile
        self.filename = infile.name
        self.metafilename = self.filename + '.yml'
        self.data = self.parse()

        # Open metadata
        try:
            with open(self.metafilename, 'r') as stream:
                try:
                    self.metadata = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
        except FileNotFoundError:
            # Use defaults:
            self.metadata = {'collection' : os.path.join(environ['HOME'], '.local/share/Anki2/User 1/collection.anki2'),
                             'deck' : os.path.basename(os.path.splitext(self.filename)[0])}


    def parse(self):
        # init
        res = []
        q = {} # current question
        incodeblockp = 0 # tracks whether we are in a code block, where spaces are allowed
        state = pstate.outside

        # read all lines
        for l in self.file.readlines() + ['\n']: # add extra newline to finish last question
            # The separator:
            if l == '\n':
                if state != pstate.outside and incodeblockp == 0: # this is the end of an answer
                    if 'answer' in q:
                        q['answer'] = q['answer'].strip()
                        res.append(q)
                        q = {}
                        state = pstate.outside
                if incodeblockp == 1:
                    q['answer'] = q.get('answer', '') + '\n'
            else:
                if state == pstate.outside or state == pstate.preamble: # still parsing metadata
                    state = pstate.preamble # we are now in the preamble of a question
                    if l.startswith("uuid "):
                        q['uuid'] = l[5:].strip()
                    elif l.startswith("id "):
                        q['id'] = l[3:].strip()
                    elif l.startswith("anki-guid "):
                        q['anki-guid'] = b32strde(l[10:].strip())
                    else:
                        q['question'] = l.strip()
                        state = pstate.answer
                elif state == pstate.answer: # have already seen the question
                    q['answer'] = q.get('answer', '') + l
                    if l.startswith('```'):
                        incodeblockp = (incodeblockp + 1) % 2
        return res


    def asNotesCollection(self):
        return NotesCollection(self.data,
                               NotesCollectionMetadata(**self.metadata))
