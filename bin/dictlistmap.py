# Map over all the string in the strange data structure that I have set up:
# EXERCISE = {QUESTION, ANSWER, REF}  (so a dictionary)
# QUESTION = STR | LIST OF EXERCISES

def dictlistmap(fun, dic):
  for k, v in dic.items():
    if isinstance(v, list):
      dic[k] = (dictlistmap(fun, w) for w in v)
    elif (dic[k] and isinstance(dic[k], str)):
      dic[k] = fun(v)
  return dic
