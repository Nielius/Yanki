import argparse
import yaml
import jinja2
from subprocess import call

parser = argparse.ArgumentParser()
parser.add_argument('--template',
                    help="use given file as a jinja2 template file",
                    default='latex-template.tex')
args = parser.parse_args()

inputfilename = "perverse-sheaves.yml"
outputfilename = "questions.tex"

with open(args.template) as templatefile, \
     open(inputfilename) as inputfile, \
     open(outputfilename) as outputfile:
    qs = yaml.load_all(inputfile)



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


# write everything to the file
for line in headerfile:
    outputfile.write(line)

for exc in qs:
    printExercise(exc)

for line in footerfile:
    outputfile.write(line)

outputfile.close()
inputfile.close()
headerfile.close()
footerfile.close()

# tmpl = jinja2.Template("""
# {% for exc in exclist %}
#  Question: {{ exc['question'] }}
# {% endfor %}
# """)
