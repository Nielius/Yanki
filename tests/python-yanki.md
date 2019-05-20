Merge two dictionaries into one, creating a new one, using unpacking.
unpack with `{**x, **y}`
(where `x` and `y` are dictionaries)

Check if a key `k` is in a dictionary `x`.
`k in x`.

Loop over all keys in a dictionary `x`.
`for k in x.keys()`

Loop over all values in a dictionary `x`.
`for v in x.values()`

Loop over all (key,value) pairs of a dictionary `x`.
`for k, v in x.items()`
N.B.: an analogy to looping over (index, value)-pairs of a list,
you could think that `enumerate(x)` might work;
however, this gives pairs of `(index, key in the dictionary)`, i.e.,
the value of the dictionary is not there.

Loop over pairs of value and index in a list.
`for index, value in enumerate(somelist)`.

Return the last item of a list.
``` python
a[-1]
```

What is python's equivalent of null?
`None`.

How do you test if something is null?
`v is None`.

Find the length of a list.
`len(l) # l a list`

Sort a list.
`l.sort() # l a list; destructive (changes the list)`

What does `a = []` and then `a[10]` give?
``` python
a = []
# raises IndexError:
a[10]
# raises IndexError:
a[10] = 'lorem'
```

Find the index of an element in a list.
```python
a = ['x', 'y', 'y', 'z']

# raises ValueError if not found:
a.index('y')
```

Get element index in array after i and before j.
`s.index(x, i, j)`

Count occurences of `x` in list `s`.
`s.count(x)`

Get min/max in list.
`min(s); max(s)`

Slice with steps.
`s[i:j:k]; s[i::k]`.
This starts at `s[i]` and goes until (but *not* including) `s[j]`,
with increments of size `k`.
Note that `k` can also be negative, in which case `j` should be lower than `i`, e.g.
`s[10:4:-2]`.

If `s` is a list with at least 5 elements, how many elements does `s[0:4]` contain?
4, because `s[4]` is *not* included.

Concatenate two lists. Give two ways: one that creates a new list and another that modifies a list to make it longer.
``` python
a = [1, 2, 3]
a2 = a + [4, 5, 6] # this creates a new list
a.extend([4, 5, 6]) # this changes the list a
```

How do you flatten a list of lists? I.e., given a list of lists, turn it into one big list by putting one after the other.
Several possibilities:
``` python
l = [[1,2,3], [4,5,6], [7,8,9]]# l is some list of lists

# using chain from itertools
from itertools import chain
chain(*l) # need to unpack the list

# using a double list comprehension
[elt for sublist in l for elt in sublist]

# using a reduce statement
reduce(list.__add__, (list(mi) for mi in list_of_menuitems))
```
See [SO](https://stackoverflow.com/questions/406121/flattening-a-shallow-list-in-python).

Can you add lists: `l1 + l2`. But suppose you want to isolate the `+` of a list, for example, to give it as an argument to a reduce. How do you do that?
With `list.__add__`.

Given two lists `a` and `b`, what is the difference between `a.extend(b)` and `a = a + b`?
In Python, it is often important to consider which operations
produce new objects and which operations change a (mutable) object.
As an example, suppose we have two lists,
`a` and `b`.
Then `a.extend(b)` changes the list `a`,
whereas `a = a + b` creates a new list and stores it in `a`.
The result in `a` is (almost?) the same,
but the memory usage is different.

How do you nest two list comprehensions?
For example, like this:
`[elt for sublist in l for elt in sublist]`.
The way I remember this, is as follows:
``` python
[elt for sublist in l
     for elt in sublist]
```
so this is in the same order as the non-comprehended for-loops:
``` python
res = []
for sublist in l:
   for elt in sublist:
      res.append(elt)
```

Manipulate the back of an array.
```python
a = [6, 7, 8]
a.append(9)
a.pop()
```

Manipulate front of an aray.
``` python
a = [6, 7, 8]
a.insert(0, 5)
a.pop(0)
```

Test membership of a list.
`7 in a` (where `a` is a list).

Make a shallow copy of a list.
Use `copiedlist = origlist.copy()`
or `copiedlist = list(origlist)`.

Make a deep copy of a list.
``` python
import copy
a = [1,2,[3,4]]
a2 = a
a3 = list(a)
a4 = copy.deepcopy(a)
```

Read a line from stdin.
``` python
line = sys.stdin.readline()
s = line.rstrip('\r\n')
```
Note that this is the same as reading a line from any file.

Write to stderr.
``` python
 	sys.stderr.write('bam!\n')
```

Open a file for reading, using `utf-8`.
``` python
 	f = open('/etc/hosts', encoding='utf-8')
```

Open a file for binary reading.
``` python
f = open('/etc/hosts', 'rb')
```

Open a file for reading and writing.
``` python
f = open('/etc/hosts', 'r+')
```

Using argparse, how do you add an optional flag that toggles something (it should be true or false)?
`parser.add_argument('-w', action='store_true')`

Read a line from a file.
``` python
f.readline()
```

Loop over all lines in a files.
``` python
for line in f:
  print(line)
```

Get all lines in a file as a generator object.
``` python
f.readlines()
```

Read an entire file into a string.
``` python
s = f.read()
```

Read a fixed length string from a file.
``` python
s = f.read(100)
```

Write and read serialized data.
``` python
import pickle

with open('/tmp/data.pickle', 'wb') as of:
  pickle.dump(somedata, of)

with open('/tmp/data.pickle', 'rb') as f:
  data = pickle.load(f)
```
Note: it seems important that you open the files as binary files
(with `wb` or `rb`).

Open a file for appending, binary writing, writing `utf-8`.
``` python
f = open('/tmp/err.log', 'a')
f = open('/tmp/test', 'wb')
f = open('/tmp/test', 'w'
  encoding='utf-8')
```

Go to a certain position in a file.
``` python
f.tell() # returns current position
f.seek(0)
```

Check (1) if a path exists; and (2) if it is a file.
``` python
os.path.exists('/etc/hosts')
os.path.isfile('/etc/hosts')
```

Get the command line arguments and the script name.
``` python
sys.argv[1:]
sys.argv[0]
```

Load a library from a subdirectory.
``` python
# foo must contain __init__.py file
import foo.bar
```

Import everything from a library.
`from mylib import *`.

Load a library from a specific path.
``` python
sys.path.append('/some/path')
```

Rename namespaces and idenitifers of imports.
``` python
# rename namespace:
import foo as fu
# rename identifier:
from sys import path as the_path
```

Create new instances of a class.
``` python
i = Int()
i2 = Int(7)
```

Define a class variable.
``` python
class Foo:
  instances = 0
```

Get and set class variables.
``` python
class Foo:
  def init(self):
    Foo.instances += 1
```

Write a class destructor.
``` python
 	def __del__(self):
        print('bye, %d' % self.value)
```

Write a subclass.
``` python
class Counter(Int):

  instances = 0

  def __init__(self, v=0):
    Counter.instances += 1
    Int.__init__(self, v)

  def incr(self):
    self.value += 1
```

Inspect a class: get the class of a class instance, and give a function to check whether an object is an instance of a specific class.
``` python
o.__class__ == Foo
isinstance(o, Foo)
```

List the basic types in python.
``` python
NoneType
bool
int
long
float
str
SRE_Pattern
datetime
list
array
dict
object
file
```

Inspect class hierarchy.
``` python
o.__class__.__bases__
```

Check if an object has a specific method.
``` python
hasattr(o, 'reverse')
```

List all attributes of an object.
``` python
 	dir(o)
```

List all loaded namespaces.
``` python
dir()
```

Inspect a given namespace.
``` python
import urlparse

dir(urlparse)
```

Get the doc string.
``` python
o.__doc__

# Or:
import inspect
inspect.getdoc(o)
```

Get the source of an object.
``` python
import inspect
inspect.getsource(o)
# getsourcefile getsourcelines also work
```

Construct a generator `firstn(n)` for the first n integers.
``` python
def firstn(n):
    num = 0
    while num < n:
        yield num
        num += 1
```

Profile a script.
`python -m cProfile -o <out.profile> <script>`

How do you unpack an argument list or a dictionary? (Pass the elements of a list as arguments to a function.)
Using `*` for the list and `**` for the dictionary (which becomes keyword arguments).

How do you define a function that takes an arbitrary number of arguments? And an arbitrary number of keyword arguments? (Variadic functions; variable number of arguments.)
```python
def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])

cheeseshop("Limburger", "It's very runny, sir.",
           "It's really very, VERY runny, sir.",
           shopkeeper="Michael Palin",
           client="John Cleese",
           sketch="Cheese Shop Sketch")
```

How do you define a decorator?
You define a function that returns a function.
```python
def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])

cheeseshop("Limburger", "It's very runny, sir.",
           "It's really very, VERY runny, sir.",
           shopkeeper="Michael Palin",
           client="John Cleese",
           sketch="Cheese Shop Sketch")
```

How do you use a decorator?
You define a function `mydecorator` that returns a function.
Then you use it as follows:
```python
@mydecorator
def decoratedFunction():
	...
```

What is the `@`-syntax before a function definition?
Decorators.

How do generators work? (In particular, how do you use and define them?)
Generators are a kind of iterators.
You define them as you would define a function,
but instead of a return, it has a `yield`:
this gives the generated value.
Generating the next value means that the function continues where it left when `yield` was called.

What are generator expressions?
`generator = (i*i for i in range(a, b))`

How do you implement an iterator class?
To add iterator behaviour to a class,
you define a `__iter__()` method,
which return an object which needs to have a `__next__()` method.
If the class itself has a `__next__()` method,
you can simply define `__iter__()` as the function that returns `self`.

How do you do multiple inheritance in python?
`class DerivedClassName(Base1, Base2, Base3):`

How do you map a function over a list in python? (Two ways.)
``` python
map(lambda x: x * x, [1, 2, 3])
# or use list comprehension:
[x * x for x in [1, 2, 3]]   
```

How do you filter a list? (Two ways.)
``` python
filter(lambda x: x > 1, [1, 2, 3])
# or use list comprehension:
[x for x in [1, 2, 3] if x > 1] 	
```

How do you reduce a list in python?
``` python
# import needed in Python 3 only
from functools import reduce

reduce(lambda x, y: x + y, [1, 2, 3], 0)
```

How do you do universal and existential test?
```python
all(i % 2 == 0 for i in [1, 2, 3, 4])
any(i % 2 == 0 for i in [1, 2, 3, 4])
```
Note that it is best to use a generator comprehension (as is done here)
and not a list comprehension, because the list would be constructed
in its entirety before `any` or `all` is applied.

How do you do variable interpolation in strings?
``` python
count = 3
item = 'ball'
print('{count} {item}s'.format(
  **locals()))
  
# Python 3.6:
print(f'{count} {item}s')
```

How do you do expression interpolation in strings?
```python
'1 + 1 = {}'.format(1 + 1)

# Python 3.6:
f'1 + 1 = {1 + 1}'
```

How do you do string formatting?
```python
'lorem %s %d %f' % ('ipsum', 13, 3.7)

fmt = 'lorem {0} {1} {2}'
fmt.format('ipsum', 13, 3.7)
```

Format a float.
`f'{math.pi:.{3}}'`

Convert a number to a string.
`'value: ' + str(8)`

Join a list of strings.
`' '.join(['do', 're', 'mi', 'fa'])`

Get dict key with default, to avoid KeyError.
`d.get('t', None)`

Delete an entry of a dictionary.
`d = {1: True, o: False}; del d[1]`

Remove an element from a list.
You can either use `mylist.pop(index)` to return the value and remove it
(`mylist.pop()` removes the last), or use `mylist.remove(someval)`
to remove the first item of the last with value `someval`.

Merge two dictionaries.
`d1.update(d2)`

Dictionary comprehension.
`to_let = {v: k for k, v in to_num.items()}`

Get keys and values of a dictionary `d` as iterators.
`d.keys(); d.values()`

Create dictionary from lists.
```python
a = [['a', 1], ['b', 2], ['c', 3]]
d = dict(a)

a = ['a', 1, 'b', 2, 'c', 3]
d = dict(zip(a[::2], a[1::2]))
```

Dictionaries with default values.
``` python
from collections import defaultdict

counts = defaultdict(lambda: 0)
counts['foo'] += 1

class Factorial(dict):
  def __missing__(self, k):
    if k > 1:
      return k * self[k-1]
    else:
      return 1

factorial = Factorial()
```
Note that the argument of `default_dict` should be a function that takes no arguments
and produces the default value.

Define a function with private state.
```python
# state not private:
def counter():
  counter.i += 1
  return counter.i

counter.i = 0
print(counter())
```

Define a (function) closure.
``` python
def make_counter():
  i = 0
  def counter():
    # new in Python 3:
    nonlocal i
    i += 1
    return i
  return counter

nays = make_counter()
print(nays())
```

Invoke operators like a function.
```python
import operator

operator.mul(3, 7)

a = ['foo', 'bar', 'baz']
operator.itemgetter(2)(a)
```

What do `with`-statements do?
Context management.

How do you define a context manager?
Make a class with `__enter__()` and `__exit__()`
or use the [`contextlib`](https://docs.python.org/3/library/contextlib.html) library.

What does the else clause in a `try ...` statement do?
It is code that is executed when no error has occured.
It is optional.
It is better to place code in the `else` clause then in the `try` part,
to better be able to locate where the error has occurred,
and to not catch the wrong kind of exception.

What does the finally clause do in a `try ...` statement?
A *finally clause* is always executed before leaving the try statement, whether an exception has occurred or not. When an exception has occurred in the try clause and has not been handled by an except clause (or it has occurred in an except or else clause), it is re-raised after the finally clause has been executed. The finally clause is also executed “on the way out” when any other clause of the try statement is left via a break, continue or return statement.

Raise an exception. What is the internal working of an exception? How do you make your own?
``` python
raise Exception('bad arg') # Here `Exception` is a class.
```
`raise ValueError('A very specific bad thing happened.')`
The way this works, is that `ValueError` is a class that inherits from `Exception`.
You're just calling its initalization function (I think).
All exceptions must be derived from the class `BaseException`,
but it is encouraged to derive from `Exception`.

Handle a specific exception.
``` python
try:
  raise Bam()
except Bam as e: # Bam is the class of the exception (defined as `class Bam(Exception): ...`)
  print(e)
```

When handling errors, how do you write one block that handles errors of three different kinds (e.g., `RuntimeError`, `TypeError` and `NameError`)?
```python
except (RuntimeError, TypeError, NameError):
    pass
```

Catch-all handler (catch any kind of exception).
``` python
try:
  risky()
except:
  print('risky failed')
```

Define a new exception.
``` python
class Bam(Exception):
  def __init__(self):
    super(Bam, self).__init__('bam!')
```

How do you get the identity of an object in python? What is it?
`id(obj)`
Every object in python has an identity, a type and a value.
The identity never changes and you can think of it as the object's address in memory.

How do you get the type of an object in python?
`type(obj)`

How do you define a destructor of a class?
Give it a `__del__` method.

Check that two objects are the same (have the same identities; not just that their values are the same).
Use `is` instead of `==` ( `is` is for identity `==` is for value).

How do you open a file for reading and writing? To append?
For reading and writing: `open(filename, "r+")`.
For reading and writing if the file possibly does not exist: `open(filename, "r+")`.
For appending: `open(filename, "a")`.

How do you read a file and then overwrite it?
```python
with open(filename, "r+") as f:
    data = f.read()
    f.seek(0)
    f.write(output)
    f.truncate()
```
This last step, `f.truncate()`, truncates the file at the current position
(i.e., everything that follows, is deleted).
You could also call it with `f.trucate(10)`, to truncate everything after the 10th character.

Turn a value into a boolean.
`bool(val)`

How do you start to debug a python program?
`python -m pdb programtodebug.py`;
or place a breakpoint in the code:
`import pdb; pdb.set_trace`
or (in python >= 3.7) `breakpoint()`;
or post-mortem: `pdb.pm()`;
or from repl: `pdb.run('mymodule.test()')`.

Split a file name into the base name and the file extension.
`os.path.splitext('somefile.ext') => ('somefile', '.ext')`.

What is the basename of a file or directory? How do you get it from a string?
The basename of a path (to a file or directory)
is the name of the file or directory without the leading directories.
For example:
```example
$ basename /home/jsmith/base.wiki 
base.wiki

$ basename /home/jsmith/
jsmith

```
In python, you can get it with
`os.path.basename(filename)`.

What is the syntax for an `if`-expression (not `if`-statements)?
`expression_if_true if condition else expression_if_false`

How do you test whether an object/class instance has an attribute? How do you get it (with a default value)?
`hasattr(obj, 'someattribute')`
and
`getattr(obj, 'someattribute', defaultvalue)`

How do you check if a string starts with or ends with a certain substring?
```python
if myStr.startswith("Yes"):
    return "Yes"
elif myStr.startswith("No"):
    return "No"
```

How do you write a function (or method) that does not do anything?
```python
def unimplementedFunction():
	pass
```

Reverse a list in two ways (creating new or in-place).
`lst[::-1]` to create new (slicing always creates new) (or `reversed(lst)` for a functional alternative)
or `list.reverse()`.

How do you prematurely exit a for loop?
You can "break out of" a for loop using `break`.
So in the for loop you can have something
`if condition:
  break`
and then you exit the for loop.
Compare with `continue`.

In a for loop, how do you interrupt the normal flow and continue to the next iteration of the loop?
Using `continue`. Compare with `break`.

Give an example of a function definition with type annotation.
`def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode`:
where `ListNode` is some class.

What is the type annotation for a function that does not return anything?
Use `-> None`.
See [PEP 0484](https://www.python.org/dev/peps/pep-0484/#using-none)
or [StackOverflow](https://stackoverflow.com/questions/36797282/python-void-return-type-annotation)

How do you give type annotations for lists of certain things?
First `from typing import List` and then `List[int]` for example.

What are functional ways to sort and reverse a list?
`sorted(somelist)` and `reversed(somelist)`
are functional versions of `somelist.sort()` (changes the list)
and `somelist.reverse()`.
These have the additional useful property that they return iterators,
so it should be lazy.

How does python `reduce` work? In which package is it? What are the arguments?
The function `reduce` is in the `functools` package and takes the following arguments:
`functools.reduce(function, iterable[, initializer])`.
The argument `function` should be a function that takes two arguments:
the first being the accumulator, the second the next item in the list.
If the optional argument `initializer` is not given,
then the first value for the accumulator is simply the first element from the list.
It is roughly equivalent to:
``` python
    def reduce(function, iterable, initializer=None):
        it = iter(iterable)
        if initializer is None:
            value = next(it)
        else:
            value = initializer
        for element in it:
            value = function(value, element)
        return value
```

Generate a random integer between 12 and 27 (inclusive).
Import `random` and run `random.randint(12,27)`.

Insert an element in a list, at a given position.
`mylist.insert(position, value)`.
The new element ends up before `mylist[position]`,
so that e.g. `mylist.insert(0, 2)` adds 2 to the start of the list.

Explain and give an example of using a `nonlocal` variable.
The nonlocal statement causes the listed identifiers to refer to previously bound variables in the nearest enclosing scope excluding globals. This is important because the default behavior for binding is to search the local namespace first. The statement allows encapsulated code to rebind variables outside of the local scope besides the global (module) scope.
One use case is in nested functions:
``` python
x = 0
def outer():
    x = 1
    def inner():
        # Three options:
        # (1) nothing
        # (2) nonlocal x
        # (3) global x
        x = 2
        print("inner:", x)

    inner()
    print("outer:", x)

outer()
print("global:", x)

# Three different kinds of output
# OPTION     (1)  (2)  (3)
# (expl)     () (nloc) (globl)
# inner:      2    2   2  
# outer:      1    2   1
# global:     0    0   2
```

Given a list `fruitlist` of strings, how do you count how often the string 'apple' occurs?
`fruitlist.count('apple')`.
See [python reference](https://docs.python.org/3/tutorial/datastructures.html) on lists.

How do you take the union of two sets? The complement of one in another? The intersection? The symmetric difference?
Suppose `a` and `b` are sets.
Then the syntax is mostly as if we're doing bit operations:
``` python
a - b   # diff; letters in a but not in b
a | b   # union; letters in a or b or both
a & b   # intersection; letters in both a and b
a ^ b   # symdif; letters in a or b but not both
```

What is this syntax? `a = {x for x in 'abracadabra' if x not in 'abc'}`
Set comprehension.

How do you test if one set is a subset or superset of another?
``` python
issubset(other)
set <= other
set < other
issuperset(other)
set >= other
set > other
```

What objects can be used as dictionary keys and set members?
Hashable objects, which are objects that have
a non-chaning hash value
(calculated by a `__hash__()` method)
and can be compared to other objects
(i.e., they have an `__eq__` method; equal implies same hash).

Are all builtins hashable? Are instances of user-defined classes hashable?
All immutable built-ins are hashable; mutable containers are not.
Objects which are instances of user-defined classes are hashable by default,
with hash derived from `id()` and are only equal to themselves.

How are sets implemented internally?
As dictionaries with dummy values, with some optimizations.

What does the `setdefault` method of a dictionary do? What are the arguments
If the key does not exist, set it with default; otherwise, do nothing.
Return final value of key.
From the [manual](https://docs.python.org/3/library/stdtypes.html#frozenset):
`setdefault(key[, default])`:
if key is in the dictionary, return its value. If not, insert key with a value of default and return default. default defaults to None.

How do you use a dictionary with default values? For example, every default value should be an empty list.
`from collections import defaultdic` and then make one with
`allwires = defaultdict(list)`.
[Documentation](https://docs.python.org/3.7/library/collections.html#collections.defaultdict)

How do you count unique values in python?
Possibility one: turn it into a set and use `len`,
e.g. `len(set(somelist))`.

How do you add or remove things from a set?
`set.add(someelt)` and `set.remove(someelt)`

How do you take and remove an element from a set?
`someelt = someset.pop()`

How do you take `xor` of two bools?
Two ways: `(cond1) ^ (cond2)`
or `(cond1) != (cond2)`;
but make sure both are `bool`s
(possibly just by using `bool(...)`).

How do you express binary literals?
With e.g. `0b101101`.

What is a `ChainMap`? In what package is it? What happens when you look up something? What happens when you update something?
A `ChainMap` (from `collections`) groups multiple dicts
(or other "mappings") together to create a single, updateable view.
It stores a (mutable) list of the mappings (in the attribute `maps`).
When you search for a key, it looks in all the mappings
and takes the first one.
If you modify (update, write or delete) something, only the first mapping is updated.
For example:
``` python
baseline = {'music': 'bach', 'art': 'rembrandt'}
adjustments = {'art': 'van gogh', 'opera': 'carmen'}
cm = ChainMap(adjustments, baseline)
```
The value of `cm['art']` is now `'van gogh'` (it first finds the value from adjustments).
The value of `music` is taken from `baseline`
(because `adjustments` does not have a key `music`).
This is useful for overshadowing defaults, for example.
See the [documentation](https://docs.python.org/3/library/collections.html#collections.ChainMap).

Given a list, how do you produce an object that counts how often each element appears in the list?
With `Counter` from `collections`.
Use the list (or other iterable) as argument in the constructor:
Examples:
``` python
>>> c = Counter()                           # a new, empty counter
>>> c = Counter('gallahad')                 # a new counter from an iterable
>>> c = Counter({'red': 4, 'blue': 2})      # a new counter from a mapping
>>> c = Counter(cats=4, dogs=8)             # a new counter from keyword args
```
Setting a count to zero does not remove an element from a counter. Use del to remove it entirely:
``` python
>>> c['sausage'] = 0                        # counter entry with a zero count
>>> del c['sausage']                        # del actually removes the entry
```
Has a useful `most_common()` method.

What is a `deque`? What package is it in? What are the most useful functions?
It is a generalization of a stack and a queue:
it supports fast push and pop on both sides
(with `append(x)/appendleft(x)` and `extend(iterable)/extendleft(iterable)`,
`pop(), popleft()` as functions).
Also has `reverse()` and `count(x)`.

What is `super()` in a python class?
`super([type[, object-or-type]])` returns a
proxy object that delegates method calls to a parent or sibling class of type.
This is useful for accessing inherited methods that have been overridden in a
class. The search order is same as that used by getattr() except that the type
itself is skipped.
Example:
``` python
class C(B):
    def method(self, arg):
        super().method(arg)    # This does the same thing as:
                               # super(C, self).method(arg)

```

What is in the python standard library for a heap? Is it a min heap or a max heap? How do you get the other kind?
You use `import heapq`.
Then you simply make a list `myheap = []`
and use `heapq.heappush(myheap, 5)` and `heapq.heappop(myheap)`.
You can also `heapq.heapify(anylist)`.
This is always a *min-heap*.
To get the other, there are 2 solutions (found on [stackoverflow](https://stackoverflow.com/questions/2501457/what-do-i-use-for-a-max-heap-implementation-in-python)):
1. Just negate the integers (replace 5 by -5).
2. Wrap whatever you're heaping in a (another) class
with a (another) `__lt__` method.

What is the `r` prefix for a string? E.g., the string `r"somestring"`?
It stands for "raw"; the entire literal is a raw string literal
and it means that backslashes are just taken as backslashes,
and not as escape characters, as they normally are.

What is a named tuple? What package do you need to import? Give an example where you make a point in the Cartesian plane into a named tuple.
`namedtuple` is a function that returns a subclass of tuple
(arguments: `namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)`)
(it does this by simply executing a string that contains a function defined).
As an example:
``` python
>>> # Basic example
>>> Point = namedtuple('Point', ['x', 'y'])
>>> p = Point(11, y=22)     # instantiate with positional or keyword arguments
>>> p[0] + p[1]             # indexable like the plain tuple (11, 22)
33
>>> x, y = p                # unpack like a regular tuple
>>> x, y
(11, 22)
>>> p.x + p.y               # fields also accessible by name
33
>>> p                       # readable __repr__ with a name=value style
Point(x=11, y=22)
```

How do you stop a python script at any point?
Using `sys.exit()`.
There is also a function `exit()`,
but it is inteded for use in the interactive shell only.
See [this question on SO](https://stackoverflow.com/questions/6501121/difference-between-exit-and-sys-exit-in-python).
