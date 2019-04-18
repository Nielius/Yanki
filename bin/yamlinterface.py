import ruamel.yaml
from ankiinterface import AnkiCollection, updateNote
from convert import convertExercise


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

class ExercisesFile:
    """A handler for a YAML file with exercises. It interprets the metadata and
    stores the list of exercises in `self.data`.

    It also has an interface to connect with the Anki database.
    The function 'connectToAnkiCollection()' does the connection
    (based on the metadata)
    and the function 'writeToAnki()' writes the data to the Anki database
    (and also updates the yaml file to contain the anki ids).
    """
    # TODO: consider implementing __setitem__, __getitem__ etc.
    # so that the ExercisesFile behaves as a list of questions
    # (with the metadata hidden from the list view)
    #

    def __init__(self, file):
        self.yamlfile = file # was: open(filename, "r+")
        self.rawdata = yaml.load(self.yamlfile) # entire yaml file
        self.metadata = self.rawdata[0] # the first entry, which is metadata

    def __del__(self):
        """(BROKEN!) Updates the yaml file to reflect the changes made in this datastructure
        (by calling self.overwriteFile) and some other clean-up."""
        # self.overwriteFile() # this doesn't work, because (I think) it relies on a global variable `yaml` that gets garbage collected earlier
        self.yamlfile.close()


    # Exercises: getAllExercises and insertExercise
    def getAllExercises(self):
        """Returns a ruamel.yaml.comments.CommentedSeq of all questions."""
        return self.rawdata[1:] # this makes a shallow copy; maybe should avoid that

    def insertExercise(self, excdict):
        """Insert an exercise. This exercise shoud simply be a dictionary,
        or possible something of type `ruamel.yaml.comments.CommentedSeq`."""
        self.rawdata.append(excdict)


    # Write to the yaml file
    def overwriteFile(self):
        """Save all the data to the yaml file."""
        self.yamlfile.seek(0)
        yaml.dump(self.rawdata, self.yamlfile)
        self.yamlfile.truncate()


    # Interface with Anki
    def connectToAnkiCollection(self, collection = None):
        """If the metadata contains a reference to an Anki collection, this sets
        self.ankicollection to an AnkiCollection class corresponding to that
        collection.

        If the optional argument 'collection' is None, then use the metadata to
        get the collection.

        In addition, if the metadata contains the description of a model (TODO!
        not implemented yet), then this model is added to the collection if it
        had not been there before. If no model is given in the metadata, the
        default Yanki-model is added.

        """
        try:
            self.ankicollection = AnkiCollection(collectionfile = (collection if collection \
                                                                   else self.metadata['collection']),
                                                 deckname = self.metadata.get('deck', None),
                                                 # Modelname is None,
                                                 # because we will manually set
                                                 # the modelname
                                                 modelname = None)
        except ValueError:
            raise Exception('Collection not defined in metadata of this YAML file.')


        if self.metadata.get('model'):
            # TODO: implement this: add or update the model given in the metadata
            self.ankicollection.selectModelByName(self.metadata.get('model'))
            pass
        else:
            # Add default model if it does not already exist
            self.ankicollection.addModel('Yanki default',
                                         ['question', 'answer', 'ref'],
                                         [{'name': 'Normal',
                                           'qfmt':  "{{question}}",
                                           'afmt':  "{{answer}}" + \
                                           "{{#ref}}\n\n(Ref: {{ref}}){{/ref}}"
                                         }])
            self.ankicollection.selectModelByName('Yanki default')

    def writeToAnki(self, deck = None):
        """Adds/updates all exercises in the yaml file to the anki collection
        specified in the metadata.

        If the optional argument deck is given, connect to that deck.
        Otherwise, use the metadata.
        If there is no deck in the metadata either,
        try to construct a deckname from the default file.

        Any new exercises get an anki id, which is written to the yaml file.
        """
        if getattr(self, 'ankicollection', None) is None:
            self.connectToAnkiCollection()


        # Add all exercises to the Anki collection and record their anki ids.
        for q in self.getAllExercises():
            # if the exercise has already been added and needs to be updated:
            ankiid = q.get('anki-id')
            qconv = q.copy()
            convertExercise(qconv, 'html')
            if not ankiid is None:
                n = self.ankicollection.getNoteById(ankiid)
                if n is None:
                    print(f'Error! The exercise {q} has anki-id {ankiid}, but is not in the anki collection!')
                else:
                    updateNote(n, qconv)
            else:
                n = self.ankicollection.addNote(qconv, self.metadata.get('deck', None))
                q['anki-id'] = n.id

        # Write the anki ids to the yaml file.
        self.ankicollection.collection.save()
        self.overwriteFile()





# Tests:

def unitTests():
    ef = ExercisesFile('test.yaml')
    ef.data[0]['anki-id'] = 192837192837 # random
    ef.overwriteFile()


if __name__ == "__main__":
    ef = ExercisesFile('test.yaml')
    ef.writeToAnki()


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
