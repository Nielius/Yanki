import ruamel.yaml
from ankiinterface import AnkiCollection, updateNote
from convert import convertExercise

from yankiintermediate import NotesCollection, NotesCollectionMetadata

# Load the file
# f = open('test.yaml')
# data = yaml.load(f)

# Format of yaml files:
#
# List of two elements:
# First element:  Metadata
# Second element: List of questions

# Or maybe differently? Just a list, where the first element is the metadata,
# and the rest are the questions?
# And maybe make it error-friendly: the first dictionary should have 'type':'metadata'


# Could also consider using notes guid (global unique id):
# q['guidb32'] = b32encode(note.guid.encode('ASCII')).decode('ASCII')
#
# where q is one of my questions and note is of Anki's class Note


# Recurring pattern:
# check if a model/deck/field/template already exists,
# then create/update/do nothing.


yaml = ruamel.yaml.YAML()

# Exercises file should contain:
#
# - data for anki
#   - collection name
#   - deck name
#   - model name
#
# - list of exercises

# The interface should allow:
#
# - easy updates (of metadata and of exercise)
# - easy read

def notesCollectionFromYAML(yamlfile):
        self.yamlfile = file # was: open(filename, "r+")
        self.rawdata = yaml.load(self.yamlfile) # entire yaml file
        return NotesCollection(rawdata[1:],
                               NotesCollectionMetadata(**rawdata[0]))


def notesCollectionToYAMLFile(col, yamlfile):
    # Write to the yaml file
    def overwriteFile(self):
        """Save all the data to the yaml file."""
        self.yamlfile.seek(0)
        yaml.dump(self.rawdata, self.yamlfile)
        self.yamlfile.truncate()



def convertYamlFileToNewFormat(filename,
                       collection = '/home/niels/.local/share/Anki2/Tmpuser/collection.anki2',
                       deckname = 'Default',
                       modelname = 'Basic'):
    """Take a yaml file that does not have any metadata, and add the metadata."""
    f = open(filename, "r+")
    filecontent = f.read()
    f.seek(0, 0)
    yaml.dump([{'metadata': True, # if this field is present, it is not a question; should be the first dict
                'collection': collection,
                'deck': deckname,
                'model': modelname}],
              f)
    f.write(filecontent)
    f.close()
