# Implements the intermediate representation that sits between Anki and our
# output files (YAML or formatless).
#
# The class contains the following data:
#
# 1. notes --- a list of dictionaries, with each dictionary having at least a question and an answer field
# 2. metadata
#
# And has the following interfaces:
#
# 1. Import/export to YAML/formatless
# 2. Update Anki database
# 3. Get all notes, add a note, ...



import ruamel.yaml
from ankiinterface import AnkiCollection, updateNote
from convert import convertExercise

class NotesCollection:
    """Our internal representation for a collection of notes with metadata."""
    def __init__(self, notes = None, metadata = None):
        self.notes = notes if notes is not None else []
        self.metadata = metadata if metadata is not None else NotesCollectionMetadata()

    # Interface with Anki
    def connectToAnkiCollection(self, collection = None, deck = None):
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
            self.ankicollection = AnkiCollection(
                collectionfile = collection if collection is not None else self.metadata.collection,
                deckname = deck if deck is not None else self.metadata.deck,
                # Modelname is None,
                # because we will manually set
                # the modelname
                modelname = None)
        except ValueError:
            raise Exception('Collection not defined in metadata of this YAML file.')


        if getattr(self.metadata, 'model', None) is not None:
            # TODO: implement this: add or update the model given in the metadata
            self.ankicollection.selectModelByName(self.metadata.model)
            pass
        else:
            # Add default model if it does not already exist
            self.ankicollection.addModel('Yanki default',
                                         ['question', 'answer', 'ref', 'uuid'], # the fields
                                         [{'name': 'Normal',
                                           'qfmt':  "{{question}}",
                                           'afmt':  "{{answer}}" + \
                                           "{{#ref}}\n\n(Ref: {{ref}}){{/ref}}"}
                                         ] # a list of templates (each template is a card made from the fields)
            )
            self.ankicollection.selectModelByName('Yanki default')

    def writeToAnki(self, deck = None, collection = None):
        """Adds/updates all exercises in the yaml file to an anki collection.
        The target anki collection is self.ankicollection if it exists;
        otherwise, it is taken from the metadata.

        If the notes in the collection did not yet have an anki-guid field, they
        receive an anki-guid from Anki, which is stored in this collection. It is
        advisable to always follows this function with a procedure that stores
        these new ids in the input file.

        If the optional argument collection is given,
        connect to that collection.
        If the optional argument deck is given,
        add any *new* cards to that deck.
        (Old cards are updated and remain in their old deck.)
        Otherwise, use the metadata.
        If there is no deck in the metadata either,
        try to construct a deckname from the default file.

        """
        if deck is None:
            deck = getattr(self.metadata, 'deck', None)


        if getattr(self, 'ankicollection', None) is None:
            self.connectToAnkiCollection(collection = collection, deck = deck)

        # Add all exercises to the Anki collection and record their anki ids.
        for q in self.notes:
            # if the exercise has already been added and needs to be updated:
            ankiid = q.get('anki-guid')
            qconv = q.copy()
            convertExercise(qconv, 'html')
            if ankiid is not None:
                n = self.ankicollection.getNoteByGuid(ankiid)
                if n is None:
                    print(f'Error! The exercise {q} has anki-guid {ankiid}, but is not in the anki collection!')
                else:
                    updateNote(n, qconv)
            else:
                n = self.ankicollection.addNote(qconv, deck)
                q['anki-guid'] = n.guid

        # Write the anki ids to the yaml file.
        self.ankicollection.collection.save()


class NotesCollectionMetadata:
    """The metadata associated to a collection of notes."""
    # What metadata should be there?
    # collection, deck, model?

    def __init__(self,
                 model = None,
                 collection = None,
                 deck = None,
                 **kwargs):
        self.model = model
        self.collection = collection
        self.deck = deck

    def asDict(self):
        return { key: getattr(self, key) for key in ['model', 'collection', 'deck']}
        # return {'model': self.model,
        #         'collection': self.collection,
        #         'deck': self.deck}
