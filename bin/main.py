# File: latex-export.py
#
# Description:
# This is the main file in my question maker project. It converts a YAML-file
# with questions, answers and references into a nice tex file that can then be
# compiled.
#
# How it works:
# It is actually just a small wrapper script. It does the following:
# - interpret the command line argument
# - load the files
# - fill in the template with jinja2.
#
# Using the jinja2 template wasn't as easy as it sounds, because you have to
# configure the rights blocks, since latex interferes a lot with the blocks
# that are the standard definition.

import argparse
import yaml
import jinja2
from orgConverter import orgConvert
# import IPython # for debugging purposes

parser = argparse.ArgumentParser(description='''Script to apply a jinja2 template to a yaml file
  describing a set of questions, possibly with answers and references.''')
parser.add_argument('--template', '-t',
                    help="use given file as a jinja2 template file",
                    default='latex-template.tex')
parser.add_argument('--input', '-i',
                     help='A YAML file that contains questions, refs, answers.',
                     default='perverse-sheaves.yml')
parser.add_argument('--output', '-o',
                    help='the output .tex file',
                    default='questions.tex')
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
    loader=jinja2.FileSystemLoader('./'),
    # Change the default delimiters used by Jinja such that it won't pick up
    # brackets attached to LaTeX macros.
    # Stolen from http://tex.stackexchange.com/questions/40720/latex-in-industry
    block_start_string = '%{',
    block_end_string = '%}',
    comment_start_string = '%{#',
    comment_end_string = '%#}',
    variable_start_string = '%{{',
    variable_end_string = '%}}',
    autoescape=jinja2.select_autoescape(['htm', 'html', 'xml']))



# There is no such function; the easiest way to do this is to use a dict comprehension:

# my_dictionary = {k: f(v) for k, v in my_dictionary.items()}

# Map over all the string in the strange data structure that I have set up:
# EXERCISE = {QUESTION, ANSWER, REF}  (so a dictionary)
# QUESTION = STR | LIST OF EXERCISES

def dictlistmap(fun, dic):
  for k, v in dic.items():
    if isinstance(v, list):
      dic[k] = (dictlistmap(fun, w) for w in v)
    elif (dic[k] and isinstance(dic[k], str)):
      dic[k] = fun(v)
  return dic

def b64decodestring (s):
    """I only created this function because b64decode and b64encode require bytes,
not strings."""
    return bytes.decode(base64.b64decode(str.encode(s)))

def b64encodestring (s):
    """I only created this function because b64decode and b64encode require bytes,
not strings."""
    return bytes.decode(base64.b64encode(str.encode(s)))

def orgToLatex(s):
    """Convert an org string to LaTeX. For this to work, an emacs-snapshot has to
be running."""
    # should work, except that the function names are of course wrong; might
    # also need to trim the quotes from the returned string; or use princ in
    # the emacs command?
    emacsoutput = subprocess.check_output("emacsclient-snapshot -e '(base64-encode-string (org-export-string-as (base64-decode-string \"{}\") '\"'\"'latex t) t)'".format(b64encodestring(s)), shell=True) # de gekke '\"'\"' is om bash een ' door te laten geven aan emacs
    # Note: the t in emacs's base64-encode-string ensures that there are no newlines in the output.

    # now we need to format the output (which is a bytetype object of a b64 string plus newlines and quotes) and decode it
    return b64decodestring(bytes.decode(emacsoutput).strip().strip('"'))


# THE ACTUAL WORK
# -----------
with open(inputfilename) as inputfile, \
     open(outputfilename, 'w') as outputfile:
    qs = yaml.load_all(inputfile)

    # IPython.embed() # for debugging purposes

    # Convert all the org strings to latex strings
    qsconv = map((lambda x: dictlistmap(orgToLatex, x)), qs)

    jinjatemplate = jinjaEnv.get_template(args.template)
    outputfile.write(jinjatemplate.render(exclist=qsconv))




# DEPRECATED FUNCTIONS
# Mostly because they have been replace with the jinja2 template system.

# DEPRECATED --- replaced by templates
def printExercise(exc, f = outputfile):
    """Print an exercise not using templates, but directly from python."""
    # I could also use a template engine such as Jinja2, Cheetah, Django (?)
    # see for more: https://www.quora.com/What-is-a-good-templating-engine-for-Python
    # http://jinja.pocoo.org/
    headerfile = open("latex-header.tex", 'r')
    footerfile = open("latex-footer.tex", 'r')


    if not isinstance(exc, dict):
        print('ERROR: should input a dict!')
        return

    if exc.get('question'):
        if isinstance(exc['question'], str):
            f.write('\\emph{{Question}}: {}\n\n'.format(exc['question'])) # the double '{{' and '}}' are because of the '.format()' syntax

        elif isinstance(exc.get('question'), list):
            f.write("\\begin{itemize}\n")
            for exc2 in exc['question']:
                f.write("\\item")
                printExercise(exc2)
            f.write("\\end{itemize}\n")

    # format an answer if there is one
    if exc.get('answer'): # this doesn't throw an error if the key 'answer' doesn't even exist
       f.write('\\emph{Answer}:' + exc['answer'] + '\n\n')

    # format a reference if there is one
    if exc.get('ref'):
       f.write('\\emph{Reference}:' + exc['ref'] + '\n\n')

# DEPRECATED --- replaced by templates
def writeFile():
    """Do not use jinja templates, but write directly to the files."""
    # TODO: this function doesn't work and I'm probably not going to use it
    for line in headerfile:
        outputfile.write(line)

    for exc in qs:
        printExercise(exc)

    for line in footerfile:
        outputfile.write(line)
