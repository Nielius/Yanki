# convert.py
#
# Contains helper functions to convert strings from markdown to another
# filetype using pypandoc.

import pypandoc
import markdown


# |- Convert markdown string to some target file type with pandoc
def convertMarkdown(x: str, targetft: str) -> str:
    """Convert a markdown string to a string of the target filetype.
    Uses python-markdown if the target is HTML; pandoc otherwise."""
    # As a one-liner: convertMarkdownFn = (lambda x: pypandoc.convert_text(x, targetFiletype, format='md'))
    if targetft == 'html':
        # see https://python-markdown.github.io/extensions/
        return markdown.markdown(x, extensions=['markdown.extensions.fenced_code'])
    return pypandoc.convert_text(x, targetft, format='md')


def convertExercise(q, targetft):
  """Convert the fields of an exercise (a dictionary with lots of fields) to the
  target file type targetft using pandoc. Essentially, this is just some kind
  of mapcar over a dictionary.

  N.B.: this is destructive (i.e., the dictionary itself changes; the function
  does not return anything.)
  """

  for k, v in q.items():
      if isinstance(v, str):
          q[k] = convertMarkdown(v, targetft)


  # Alternative functional approach:
  # return {k: (convertMarkdown(v, targetft) if isinstance(v, str) else v) for k, v in q.items()}

