import os.path

# Small helper functions

def updatedFilename(filename):
  "Sends a filename to a new filename '-updn' where n is empty or the smallest integer that makes the filename unique."
  # See https://stackoverflow.com/questions/183480/is-this-the-best-way-to-get-unique-version-of-filename-w-python
  # for a possibly better appraoch

  base, ext = os.path.splitext(filename) # returns ('/path/file', '.ext')
  counter = 0

  newname = base + '-upd' + ext
  while os.path.lexists(newname):
    counter = counter + 1
    newname = base + '-upd' + str(counter) + ext

  return newname
