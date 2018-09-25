# Some commands that are useful to send to the REPL when testing

# Opening files
inputfilename = '../questionsets/etale-fundamental-groups-md.yaml'
outputfilename = 'deleteme-output.tex'

inputfile = open(inputfilename)
outputfile =  open(outputfilename, 'w')



yaml = ruamel.yaml.YAML()
data = yaml.load(inputfile)
data[-1]
yaml.dump(data, sys.stdout)

print(type(data['data_points']))



# Here you should do many of the things from the program


# Doing the actual conversion
jinjatemplate = jinjaEnv.get_template('answer-template.tex')
outputfile.write(jinjatemplate.render(exclist=qsconv))




import sys
sys.path.append("/home/niels/proj/anki") # this should probably not really be part of the code
from anki.storage import Collection
profileHome = "/home/niels/.local/share/Anki2/Tmpuser"
collectionPath = os.path.join(profileHome, 'collection.anki2')
col = Collection(collectionPath, log=True)
col.conf['curModel'] = 1 # this is just the basic model with only a question and an answer

note = col.newNote()
note.fields[0] = q.get('question', '') # the second is the default value if key 'question' doesn't exist
note.fields[1] = q.get('answer', '') # i.d.
col.addNote(note)


# TODO
# - [X] get the 'Basic' model
col.models.byName('Basic')['id']
# - [X] take note.guid and put it in the right place with ruamel; probably as string literal
# - [ ] write to output
#
# At a later stage: update the notes using the guids

# Options: --overwrite-yaml-input --tag (should accept a list)




import ruamel.yaml as yaml

yaml_str = """\
pubkey: >-
    -----BEGIN PUBLIC KEY-----
    MIGfMA0GCSq7OPxRrQEBAQUAA4GNADCBiQKBgQCvRVUKp6pr4qBEnE9lviuyfiNq
    QtG/OCyBDXL4Bh3FmUzfNI+Z4Bh3FmUx+z2n0FCv/4BpgHTDl8D95NPopWVo1RH2
    UfhyMd6dQ/x9T5m+y38JMzmSVAk+Fqu8ya18+yQVOEyEIx3Gxpsgegow33gcxfjK
    EsUgJHXcpw7OPxRrCQIDAQAB
    -----END PUBLIC KEY-----
"""

data = yaml.load(yaml_str, Loader=yaml.RoundTripLoader)
print(yaml.dump(data, Dumper=yaml.RoundTripDumper, indent=4))

# ----------------------------- 

import sys
import ruamel.yaml

yaml_str = """\
any_value: 123.4
data_points: >-
  a # test
  b
"""

yaml = ruamel.yaml.YAML()
data = yaml.load(yaml_str)
yaml.dump(data, sys.stdout)

print(type(data['data_points']))

from ruamel.yaml.scalarstring import PreservedScalarString

data['data_points'] = PreservedScalarString("""\
0.0, 1.0
0.1, 1.5
0.2, 1.7""")

from base64 import b32encode, b32decode

data['guid'] = PreservedScalarString("""Q&F`o~w;|1""")
data['guidb32'] = b32encode(note.guid.encode('ASCII')).decode('ASCII')
yaml.dump(data, sys.stdout)


