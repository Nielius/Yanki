import ruamel.yaml
from ankiinterface import AnkiCollection, updateNote
from convert import convertExercise

from notescollection import NotesCollection, NotesCollectionMetadata

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

def YAMLToNotesCollection(yamlfile):
    """Imports a YAML file as a NotesCollection."""
    rawdata = yaml.load(yamlfile)
    return NotesCollection(rawdata[1:], NotesCollectionMetadata(**rawdata[0]))


def NotesCollectionToYAML(col, yamlfile):
    """Saves a NotesCollection to a yaml file."""
    yamlfile.seek(0)
    metadatadict = col.metadata.asDict()
    metadatadict.update({'metadata': True}) # this is required in our syntax for YAML files
    rawdata = ruamel.yaml.comments.CommentedSeq([metadatadict])
    rawdata.extend(col.notes)
    yaml.dump(rawdata, yamlfile)
    yamlfile.truncate()



def convertYamlFileToNewFormat(filename,
                               collection,
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
