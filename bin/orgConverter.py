import base64
import subprocess

def b64decodestring (s):
    """I only created this function because b64decode and b64encode require bytes,
not strings."""
    return bytes.decode(base64.b64decode(str.encode(s)))

def b64encodestring (s):
    """I only created this function because b64decode and b64encode require bytes,
not strings."""
    return bytes.decode(base64.b64encode(str.encode(s)))

def orgConvert(s, target='latex'):
    """Convert an org string to Latex or anything else. For this to work, an emacs-snapshot has to
be running."""
    # should work, except that the function names are of course wrong; might
    # also need to trim the quotes from the returned string; or use princ in
    # the emacs command?
    emacsoutput = subprocess.check_output("emacsclient-snapshot -e '(base64-encode-string (org-export-string-as (base64-decode-string \"{}\") '\"'\"'{} t) t)'".format(b64encodestring(s), target), shell=True) # de gekke '\"'\"' is om bash een ' door te laten geven aan emacs
    # Note: the t in emacs's base64-encode-string ensures that there are no newlines in the output.

    # now we need to format the output (which is a bytetype object of a b64 string plus newlines and quotes) and decode it
    return b64decodestring(bytes.decode(emacsoutput).strip().strip('"'))
