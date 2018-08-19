# Some commands that are useful to send to the REPL when testing

# Opening files
inputfilename = '../tests/etale-fundamental-groups-md.yaml'
outputfilename = 'deleteme-output.tex'

inputfile = open(inputfilename)
outputfile =  open(outputfilename, 'w')


# Here you should do many of the things from the program


# Doing the actual conversion
jinjatemplate = jinjaEnv.get_template('answer-template.tex')
outputfile.write(jinjatemplate.render(exclist=qsconv))
