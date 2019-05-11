# base32helpers
#
# 2 small helper functions to encode and decode with b32. They wrap around the
# standard functions, but both take strings as input and also have strings as
# output.

from base64 import b32encode, b32decode

# To encode/decode strings to strings with b32
def b32stren(s):
    return b32encode(s.encode('utf-8')).decode('utf-8')

def b32strde(s):
    return b32decode(s.encode('utf-8')).decode('utf-8')
