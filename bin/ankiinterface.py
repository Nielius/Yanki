# ankiinterface.py
#
# Methods and classes to manipulate Anki databases, based partly on the code
# that Anki itself uses.

import sys

sys.path.append("/home/niels/proj/anki") # this should probably not really be part of the code
from anki.storage import Collection
from anki.models import defaultField, defaultTemplate


# Should support:
#
# - adding note (to deck? with model?)
# - updating note
# - deleting note? (specific form of update? or maybe not detect this?)
#   - maybe only keep notes that are in the yaml file?
#
# - Adding a model?

# Also need: YAMLtoAnki -interface? or functions?
# For example: the ids of the notes need to be added to the yaml file.


def updateNote(note, updict):
  """Update the note <note> according to the dictionary <updict>, i.e., for every
  (key, value) pair in <updict>, set the <key> field of <note> to <value> *if*
  there is a key field in the note's model.

  This works exactly as mydictionary.update(anotherdictionary) would,
  but the point is the the note class does not have such an update function yet.
  This serves as one, without changing the class definition.

  """
  for key, value in updict.items():
    if key in note: # does the note accept the field `key`?
      note[key] = value
  note.flush() # save to disk; not sure if this is necessary, but seems to be


class AnkiCollection():
  def __init__(self,
               collectionfile,
               deckname = None,
               modelname = None):
    """Connects to an anki collection stored in a file.
    """
    self.collection = Collection(collectionfile, log=True)
    if not deckname is None:
      deckid = self.createOrReturnDeckId(deckname)
      self.selectDeckById(deckid)

    if not modelname is None:
      self.selectModelByName(modelname)

  def __del__(self):
    self.collection.close() # this also saves the collection


  # Selecting (= make current) decks and models
  def selectDeckById(self, did):
    """Make the deck with id <did> the current deck (whatever that means)."""
    self.collection.decks.select(did)

  def selectDeckByName(self, deckname):
    deck = self.collection.decks.byName(deckname)
    # This raises a value error if the deck is not found
    self.collection.decks.select(deck['id'])

  def currentDeck(self):
    return self.collection.decks.current()

  def createOrReturnDeckId(self, name, create=True):
    "Add a deck with NAME. Reuse deck if already exists. Return id as int."
    return self.collection.decks.id(name, create)


  def selectModelById(self, mid):
    """Make the model with id <mid> the current model.
    These models specify the fields that notes have."""
    m = self.collection.models.get(mid)
    self.collection.models.setCurrent(m)

  def selectModelByName(self, modelname):
    """Set the current model to the model with name <modelname>.
    Gives an error (TypeError: 'NoneType' object is not subscriptable)
    when the model doesn't exist."""
    self.collection.models.setCurrent(self.collection.models.byName(modelname))

  def currentModel(self):
    return self.collection.models.current()

  # Adding notes
  def addNote(self, fieldsdict, deckname=None, modelname=None):
    """Add a note to the collection. The fields in the note are given by the
    dictionary <fieldsdict>. Also adds associated cards. Returns the new note.

    If the optional deck and model arguments are not given, use the current
    deck and model.

    If the arguments are given, this changes the current deck and model to the
    given arguments.
    """
    if deckname:
      self.selectDeckByName(deckname)
    if modelname:
      self.selectModelByName(modelname)

    n = self.collection.newNote()
    # set note fields
    updateNote(n, fieldsdict)
    # add all the cards for this note
    self.collection.genCards([n.id])

    # Necessary to get all cards into the right deck
    deckid = self.currentDeck()['id']
    for card in n.cards():
      card.did = deckid
      card.flush()

    return n

  def getNoteById(self, nid):
    """Returns the note with id `nid`.
    """
    # MAKE THIS SAFE!
    # Catch TypeError:
    # if the note id is not found,
    # then for some stupid reason, a TypeError is raised
    # (i.e., the anki code does not check if the note actually exists;
    # and if the database returns an empty list, a TypeError occurs)
    try:
      note = self.collection.getNote(nid)
    except TypeError:
      raise ValueError(f'The note with id {nid} does not seem to exist.')

    return note

  def getNoteByGuid(self, guid):
    """Returns the note with given guid.

    Raises an error if there is not exactly one note with that guid."""
    results = self.collection.db.list(f'select n.id from notes n where n.guid=\'{guid}\'')
    if len(results) != 1:
      raise ValueError(f'There are {len(results)} notes with guid {guid}.')

    return self.getNoteById(results[0])



  # Models

  def addModel(self, modelname: str, fieldnames: list, templatelist: list,
               failSilently: bool = True):
    """Add a model with name <modelname> to the collection.
    The variable <fieldnames> is a list of field names that the model has.
    The variable <templatelist> is a list of templates;
    each template is a dictionary that contains three fields:

    (1) 'name' --- the name of the type of card (e.g. 'Reverse' or 'Pinyin');
    (2) 'qfmt' --- the template for the question; and
    (3) 'aftm' --- the template for the answer.

    Returns the new model.

    If a model with name <modelname> already exists,
    do nothing and return that model.
    If <failSilently> is False, additionally return an error.

    Code taking mostly from Anki's own code (`stdmodels.py`).
    I do not entirely understand why all these seperate adding steps are necessary.

    (I am not sure if the collection should still be saved; I think so.
    If you close the collection, then it seems this is automatically saved.)
    """
    # Check if a model with name <modelname> exists
    m = self.getModel(modelname)
    if not m is None:
      if failSilently:
        return m
      else:
        raise Exception(f'Error: the model with name {modelname} already exists!')

    # Otherwise, make new model
    mm = self.collection.models # mm = modelmanager
    m = mm.new(modelname)

    # Add the fields
    for fieldname in fieldnames:
      newfield = mm.newField(fieldname)
      mm.addField(m, newfield)

    # Add the templates
    for template in templatelist:
      newtemplate = mm.newTemplate(template['name'])
      newtemplate['qfmt'] = template['qfmt']
      newtemplate['afmt'] = template['afmt']
      mm.addTemplate(m, newtemplate)

    # Add the model
    mm.add(m)

    return m

  def getModel(self, modelname: str):
    """Returns the model with name <modelname>, if it exists.
    If it does not exist, return `None`.
    """
    return self.collection.models.byName(modelname)




# Tests

if __name__ == "__main__":

  testdict = {
    'Hanzi':	'this is Hanzi testietessdfoijt',
    'Pinyin': 'this is the new pinyin ijoijoasidjfoasijd',
    'English': 'this is the new Englbasdfish'
  }


  newnote = mcol.addNote(testdict, modelname='Chinese', deckname='Default')

  mcol = AnkiCollection()
  newmodel = mcol.addModel('Yanki default',
                           ['question', 'answer', 'ref'],
                           [{'name': 'Normal',
                             'qfmt':  "{{question}}",
                             'afmt':  "{{answer}}" + \
                             "{{#ref}}\n\n(Ref: {{ref}}){{/ref}}"
                           }])


  mcol.addModel('Yanki default', ['test'], [], failSilently=False)
