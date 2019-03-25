# quickconvert.py
#
# The purpose of this code is to generate YAML files for my yanki application
# from files that have a very easy format, described below.
#
# Format of the input:
#
# - all exercises are separated by a newline
# - the first line of an exercises is the question; the other lines form the answer
# - newlines inside markdown code blocks are not interpreted as separators of exercises;
#   all other newlines are.


from ruamel.yaml import YAML
import ruamel
import sys
import os.path

yaml = YAML()
yaml.block_indent = 4
yaml.indent = 4

# These next two lines allow us to specify that certain strings need to be
# represented using blocks in yaml. Code taken from
# https://stackoverflow.com/questions/6432605/any-yaml-libraries-in-python-that-support-dumping-of-long-strings-as-block-liter
folded = ruamel.yaml.scalarstring.FoldedScalarString
literal = ruamel.yaml.scalarstring.LiteralScalarString



if len(sys.argv) > 1:
    fn = sys.argv[1]
else:
    fn = 'input.md'
f = open(fn)



# More imperative style

# The first element of the list should be some metadata:
qs = [{'metadata': True, # if this field is present, it is not a question; should be the first dict
       'collection': '/home/niels/.local/share/Anki2/Tmpuser/collection.anki2',
       'deck': os.path.basename(os.path.splitext(fn)[0])}]
q = {}
busy = 0 # tracks whether we were busy reading a question
firstline = 1 # tracks whether this is the first line of a question
incodeblock = 0 # tracks whether we are in a code block, where spaces are allowed
for l in f.readlines():
    if l == '\n':
        # New line: if we were considering a question, this finishes the
        # question. Otherwise, just ignore.
        if busy == 1 and incodeblock == 0: # this is the end of an answer
            if 'answer' in q:
                q['answer'] = literal(q['answer'].strip())
            qs.append(q)
            q = {}
            busy = 0
            firstline = 1
        if incodeblock == 1:
            q['answer'] = q.get('answer', '') + '\n'
    else:
        if firstline == 1:
            q['question'] = literal(l.strip())
            firstline = 0
            busy = 1
        else:
            q['answer'] = q.get('answer', '') + l
            if l.startswith('```'):
                incodeblock = (incodeblock + 1) % 2

if busy == 1:
    q['answer'] = literal(q['answer'].strip())
    qs.append(q)


yaml.dump(qs, sys.stdout)
# or maybe yaml.round_trip_dump()?
