# formatless.py
#
# Parse a "formatless" file.
#
# "Formatless" is a file syntax that is not so expressive, but expressive
# enough for basic yanki cards. They seem to be what I will need most anyway.
#
# A possible (as of yet unimplemented) extension would be to have a formatless
# file together with a metadata file. This metadata file could be more
# complicated (e.g. YAML or sexps) and use the IDs of the cards in formatless
# to express more difficult relations (such as hierarchies of the notes, or
# general metadata).
#
# Informal specification of the syntax:
#
# 1. Questions are separated by newlines (except for newlines within code
# blocks).
#
# 2. The first line that does not start with 'id ' is the question. The
# question is always only one line.
#
# 3. Everything that follows the question, is the answer.
#
# 4. Questions may optionally start with 'id [id]' to denote the id.
#
# 5. There are no escape sequences. The only special situation is markdown code
# blocks, which start with '```' on a line and end with a line that is only
# '````.
#
#
# Usage of the Formatless class:
#
# - `Formatless.__init__(self, filename)`: open and parse a file with formatless syntax
# - `Formatless.writeToFile(self, filename)`: write the data to a formatless file
# - `writeListToFormatless(data, outfile)`: write any list of question, answer and id to outfile in formatless syntax

from enum import Enum

# To track the state of the parser:
pstate = Enum('Parser state',
              'preamble ' + # ids and probably other metadata of the function
              'question ' + # reading the question
              'answer ' + # reading the answer
              'outside') # not reading a question

def writeListToFormatless(data, outfile):
    """Write a data (a list of dictionaries (with (optionally) id, question,
    answer)) to outfile as a formatless file.

    """
    for exc in data:
        if 'id' in exc:
            outfile.write('id ' + exc['id'])
        if 'question' in exc:
            outfile.write(exc['question'] + '\n')
        else:
            raise ValueError('This exercise does not have a question!')
        if 'answer' in exc:
            outfile.write(exc['answer'] + '\n')
        outfile.write('\n')


class Formatless:
    """Parses formatless files."""

    def __init__(self, filename):
        """Initializes a file with formatless syntax: opens the file, parses it, and
        stores the resulting list of dictionaries (with question, answer and
        possibly id) in `self.data`.
        """
        # TODO: wrong pattern! input should just be a file handler *OR* a filename
        # I think there was something smart for that.
        self.filename = filename
        self.file = open(filename, 'r')
        self.data = self.parse()

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
                if state == pstate.outside and l.startswith("id "):
                    q['id'] = l[3:].strip()
                    state = pstate.preamble
                elif state == pstate.outside or state == pstate.preamble:
                    q['question'] = l.strip()
                    state = pstate.answer
                elif state == pstate.answer:
                    q['answer'] = q.get('answer', '') + l
                    if l.startswith('```'):
                        incodeblockp = (incodeblockp + 1) % 2
        return res

    def writeToFile(self, outfile):
        """Write the data of this formatless file to the file outfile."""
        writeListToFormatless(self.data, outfile)


# Testing suite
def test():
    # Open file
    infile = '/home/niels/tmp/formatless-test-file.md'
    res = Formatless(infile)

    # Change it a bit
    for exc in res.data:
        exc['question'] = 'Huh? ' + exc['question']

    # And write it to a file
    outfile = open('/home/niels/tmp/formatless-test-file-changed.md', 'w')
    res.writeToFile(outfile)
    outfile.close()
