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
    block_start_string = '%{',
    block_end_string = '%}',
    comment_start_string = '%{#',
    comment_end_string = '%#}',
    variable_start_string = '%{{',
    variable_end_string = '%}}',
    autoescape=jinja2.select_autoescape(['htm', 'html', 'xml']))

with open(inputfilename) as inputfile, \
     open(outputfilename) as outputfile:
    qs = yaml.load_all(inputfile)

    jinjatemplate = jinjaEnv.get_template(args.template)
    outputfile.write(jinjatemplate.render(exclist=qs))



    # temp
with open(inputfilename, 'r') as inputfile, \
     open(outputfilename, 'w') as outputfile:
    qs = yaml.load_all(inputfile)

    jinjatemplate = jinjaEnv.get_template(template)
    outputfile.write(jinjatemplate.render(exclist=qs))


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
