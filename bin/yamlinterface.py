# yamlinterface.py
#
# Contains functions to interface between NotesCollection and YAML files.
#
# The YAML files are formatted as follows:
#
# Each file is a list of dictionaries. The first dictionary is a dictionary
# with metadata about the entire set of questions. (TODO: describe the values
# that are allowed.) It should have a field `metadata` with the value `True`.
#
# All other dictionaries in the list represent questions. They require at least
# the fields 'question' and 'answer'.

import ruamel.yaml
from ankiinterface import AnkiCollection, updateNote
from convert import convertExercise

from notescollection import NotesCollection, NotesCollectionMetadata
yaml = ruamel.yaml.YAML()


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
