uuid e17da856-0e91-496a-a919-65941b7d1df7
anki-guid OY7XCTJ2PAVG2JSL
Merge two dictionaries into one, using unpacking.
unpack with `{**x, **y}`
(where `x` and `y` are dictionaries)

uuid 0376b269-d890-41db-bb93-34a0388acde4
anki-guid PAVHMWDMH55S4JCI
Check if a key `k` is in a dictionary `x`.
`k in x`.

uuid 62b76de0-2573-4a37-92ac-cde13cf85289
anki-guid NVBECXLQFRMWSSY=
Loop over all keys in a dictionary `x`.
`for k in x.items()`

uuid 776e31d8-8f96-441b-af63-e48da41a4066
anki-guid OFJEG7RDLNQUU3LL
Loop over all (key,value) pairs of a dictionary `x`.
`for k, v in x.items()`

uuid 55b2e98d-3dcd-44a6-93c0-6b22e25cee7b
anki-guid J4WHUYDFOYXE4Q33
Return the last item of a list.
``` python
a[-1]
```

uuid 2e3bb38b-3c75-4bb2-945f-ca15980c44c9
anki-guid JFNVAJLDPVJD6ZZF
What is python's equivalent of null?
`None`.

uuid fab1759c-c501-4472-ac35-de99c08785eb
anki-guid NJSEYRB6FNMEOMDJ
How do you test if something is null?
`v is None`.

uuid f4d2e927-fe25-454a-8c7a-ad9650cce680
anki-guid OASHEY3BHJQDG5RP
Find the length of a list.
`len(l) # l a list`

uuid 54cc4513-4d82-4507-ac98-29ed471affe4
anki-guid NB3EO3TEFZXG46LW
Sort a list.
`l.sort() # l a list; destructive (changes the list)`

uuid 5cf0820b-4b8b-4631-bac1-c0f7a57c8784
anki-guid IR4TQWTIEZVTK533
What does `a = []` and then `a[10]` give?
``` python
a = []
# raises IndexError:
a[10]
# raises IndexError:
a[10] = 'lorem'
```

uuid 1dd18dbe-47b4-40f1-9e41-c22ff48e941e
anki-guid INTXO7CQNF4DMSDL
Find the index of an element in a list.
```python
a = ['x', 'y', 'y', 'z']

# raises ValueError if not found:
a.index('y')
```

uuid 60237f4c-54e1-4dca-8105-c0a99bb981a9
anki-guid NJLWOV3WMVAEA3JW
Get element index in array after i and before j.
`s.index(x, i, j)`

uuid e8b3a3ae-13a9-4160-a626-20b6ea016055
anki-guid OY3WQRKJGY7G6QQ=
Count occurences of `x` in list `s`.
`s.count(x)`

uuid 7c9d1e3f-82e3-4fc2-a3dd-4925c858830c
anki-guid IU3DC5DJMNXGWZLB
Get min/max in list.
`min(s); max(s)`

uuid 098dddb5-63f4-408e-943b-f305d2048fdb
anki-guid OQWWCRREN5MDYPCW
Slice with steps.
`s[i:j;k]; s[i::k]`

uuid bcb33e35-9575-44fc-b399-bf79d7a2d240
anki-guid JQ5EIVZYKISGS5CR
Concatenate two lists.
``` python
a = [1, 2, 3]
a2 = a + [4, 5, 6]
a.extend([4, 5, 6])
```

uuid 7dce3e9b-dc34-4d6a-be60-fd871763fbac
anki-guid IVZTIK32IUYUIPLR
Manipulate back of an array.
```python
a = [6, 7, 8]
a.append(9)
a.pop() 	$a = [6, 7, 8];
```

uuid d2a4c82a-dc7d-459f-8ef5-0ab5a7053b3f
anki-guid J5HFO6COGR6TIKBG
Manipulate front of an aray.
``` python
a = [6, 7, 8]
a.insert(0, 5)
a.pop(0)
```

uuid fe625165-bdfa-4e59-8b1b-fcf588a1d1b9
anki-guid JYQTEWR5OIUTQN27
Iterate over pairs of index and element in a list.
```python
a = ['do', 're', 'mi', 'fa']
for i, s in enumerate(a):
  print('%s at index %d' % (s, i)) 
```

uuid 4dc86161-2b2d-44e5-9784-d055bcd2741d
anki-guid KFXEYY2YPNIDYYS7
Test membership of a list.
`7 in a` (where `a` is a list).

uuid dde5c0a4-48c2-4289-aa00-695396d7343d
anki-guid MQYXEO33F46D2WTW
Make a deep copy of a list.
``` python
import copy
a = [1,2,[3,4]]
a2 = a
a3 = list(a)
a4 = copy.deepcopy(a)
```

uuid 3adc396e-c2e6-4018-9751-8cea053eb971
anki-guid JVDCIPSPNY3CUYQ=
Read a line from stdin.
``` python
line = sys.stdin.readline()
s = line.rstrip('\r\n')
```

uuid f1076b7b-5710-408d-83e0-1ebea0f17b19
anki-guid N4RWONBONAYCYLDL
Write to stderr.
``` python
 	sys.stderr.write('bam!\n')
```

uuid 9b68e22f-7487-4584-ac30-4160f97c5c53
anki-guid NJOSCIKBKFGUILJZ
Open a file for reading, using `utf-8`.
``` python
 	f = open('/etc/hosts', encoding='utf-8')
```

uuid 98b87bbb-ec54-4f74-8227-4dd5ade17a80
anki-guid NUUUE4KLG52HIMTH
Open a file for binary reading.
``` python
f = open('/etc/hosts', 'rb')
```

uuid fe661c14-c88e-4a90-98b7-8b1c96ffba4c
anki-guid J4RXOSJNPVTGKND3
Read a line from a file.
``` python
f.readline()
```

uuid 611f686a-0b15-447a-abce-68d19c9af913
anki-guid JNWCKZLYHAST63LS
Loop over all lines in a files.
``` python
for line in f:
  print(line)
```

uuid d14943a5-4a62-4f98-9a85-975cb253b0b2
anki-guid JNHDCSTNGNEW66LV
Get all lines in a file from as a generator object.
``` python
f.readlines()
```

uuid 2b71ef82-dfa1-4328-8b88-50b45460646e
anki-guid INTDIPLIMRWGEJL2
Read an entire file into a string.
``` python
s = f.read()
```

uuid eff660f6-7035-4952-9b8e-0cfccdca2330
anki-guid PFFHQ3CAFFHSW7KO
Read a fixed length in a file.
``` python
s = f.read(100)
```

uuid a004fc15-17c8-4c4a-b011-12736eeb9f62
anki-guid IZKHEWJJK44XM6ZF
Read serialized data.
``` python
import pickle

with open('/tmp/data.pickle', 'rb') as f:
  data = pickle.load(f)
```

uuid b4c7e161-041c-49fb-a1be-e2e997874576
anki-guid ONOXOKZVLUSDGUDC
Open a file for appending, binary writing, writing `utf-8`.
``` python
f = open('/tmp/err.log', 'a')
f = open('/tmp/test', 'wb')
f = open('/tmp/test', 'w'
  encoding='utf-8')
```

uuid c4979b90-684a-4e7a-826f-0f001af901f1
anki-guid PFSGAJCKFMWDOZCN
Go to a certain position in a file.
``` python
f.tell()
f.seek(0)
```

uuid 37582b9f-d233-4048-8a27-cd84a41296a9
anki-guid PE4F44TYGEVWUW2T
Check (1) if a path exists; and (2) if it is a file.
``` python
os.path.exists('/etc/hosts')
os.path.isfile('/etc/hosts')
```

uuid 911f957d-4659-44e4-b374-386fda8e9eaf
anki-guid KBRDWK2GJ4WVKWDV
Get the command line arguments and the script name.
``` python
sys.argv[1:]
sys.argv[0]
```

uuid e079ab92-8c09-48bf-b3f6-ff84c147b1ed
anki-guid M4TF62SOOA3FI4DT
Load a library from a subdirectory.
``` python
# foo must contain __init__.py file
import foo.bar
```

uuid 5cb123f5-16f1-4e2a-9a72-45732a7d6277
anki-guid KAXXIXJDPBYHESRY
Import everything from a library.
`from mylib import *`.

uuid 5e49f711-c198-4b3e-93e3-a4c49d657a77
anki-guid MVRH47K3MBIXA3LV
Load a library from a specific path.
``` python
sys.path.append('/some/path')
```

uuid b936058e-5c6c-4f9d-a7c0-14205b6fd854
anki-guid ONPV4SDNO5PWOTTX
Rename namespaces and idenitifers of imports.
``` python
# rename namespace:
import foo as fu
# rename identifier:
from sys import path as the_path
```

uuid 18cba7df-d4fc-4012-b1a9-b1cc0957a94b
anki-guid OM3FG3CPGZXT2MZM
Create new instances of a class.
``` python
i = Int()
i2 = Int(7)
```

uuid cc7f2728-9c21-4a6f-ba3b-47fd15c7470e
anki-guid IRLVO6BLH5XG2NDW
Define a class variable.
``` python
class Foo:
  instances = 0
```

uuid 491f3a7a-bd61-4eab-9f28-6bd1525e121c
anki-guid ORCF2V2HOIYFGW2W
Get and set class variables.
``` python
 	class Foo:
  def init(self):
    Foo.instances += 1
```

uuid 6037372d-90ac-455f-bafc-ff59483d40da
anki-guid M45S2OKFLNECYTCI
Write a class destructor.
``` python
 	def __del__(self):
        print('bye, %d' % self.value)
```

uuid 30837f66-cd9c-45c9-8816-393428942241
anki-guid JBBGONZXFJCF2ZB7
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

uuid 23279c29-a704-4884-9741-dc0d47813fa0
anki-guid OU5UI7BVGZRW4W2M
Inspect a class: get the class of a class instance, and give a function to check whether an object is an instance of a specific class.
``` python
o.__class__ == Foo
isinstance(o, Foo)
```

uuid 63b9be52-d040-441d-a9cc-ee581197c18d
anki-guid INJWS2RUNFLHOXSA
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

uuid 101d9df0-c275-42ee-a11b-c5298e272f06
anki-guid IVZUWYSTPNREMOKZ
Inspect class hierarchy.
``` python
o.__class__.__bases__
```

uuid 21e2516c-1b9f-4bb1-8c0f-dc8f6ef4e3de
anki-guid PFQCC7TMMF5EIQLT
Check if an object has a specific method.
``` python
hasattr(o, 'reverse')
```

uuid 33e329d4-78c1-4d84-9f1f-d74f85d7a713
anki-guid NNUGIYK2O5LXAZDA
List all attributes of an object.
``` python
 	dir(o)
```

uuid a84c3a16-da81-410e-893e-0b135272c459
anki-guid IFBDKW27M57ES6R2
List all loaded namespaces.
``` python
dir()
```

uuid 1980ea1d-30c6-4699-b25b-a62437305518
anki-guid MRNWCVDFHZQU6JRV
Inspect a given namespace.
``` python
import urlparse

dir(urlparse)
```

uuid c4c42afc-cd2f-424d-bf6b-5ab04842cdc8
anki-guid IMQUYIZ2PNJU4KDN
Get the doc string.
``` python
o.__doc__

# Or:
import inspect
inspect.getdoc(o)
```

uuid 821182d0-f87f-4b75-ba11-32b982507d69
anki-guid PJFS65DBJF4XGM3B
Get the source of an object.
``` python
import inspect
inspect.getsource(o)
# getsourcefile getsourcelines also work
```

uuid 7afe98e1-0e98-4acf-ac0e-0358a91ba85d
anki-guid MZLG4PK2LBRXERLQ
Construct a generator `firstn(n)` for the first n integers.
``` python
def firstn(n):
    num = 0
    while num < n:
        yield num
        num += 1
```

uuid 6a17f823-d1f8-4dc9-86dd-f1b72d2ad191
anki-guid OBPTY4ZOPRXW6M3V
Profile a script.
`python -m cProfile -o <out.profile> <script>`

uuid 55099bb5-1235-406c-bcc0-f113774ed519
anki-guid MMZDE2BMJJAC4LDY
How do you unpack an argument list or a dictionary? (Pass the elements of a list as arguments to a function.)
Using `*` for the list and `**` for the dictionary (which becomes keyword arguments).

uuid b41ce56e-3dcc-478c-bf92-099c6ec3f01b
anki-guid MJXGAM3WNV6CSXJ5
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

uuid dee20ecf-f09c-482e-922b-ca045d44be77
anki-guid NJWHOYLIPVYDKIZP
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

uuid 4fa715a7-c3ae-49eb-bedb-8536dd07710a
anki-guid JQUC4IZNFUZFKJTE
How do you use a decorator?
You define a function `mydecorator` that returns a function.
Then you use it as follows:
```python
@mydecorator
def decoratedFunction():
	...
```

uuid fc83a33c-4287-442e-b95c-087d45b86a5a
anki-guid N47XKOZBO47VMXZF
What is the `@`-syntax before a function definition?
Decorators.

uuid a13ddb15-f67e-4b1e-a2fd-a8aa05090a50
anki-guid IJ7D2OKMFB6DSVTV
How do generators work? (In particular, how do you use and define them?)
Generators are a kind of iterators.
You define them as you would define a function,
but instead of a return, it has a `yield`:
this gives the generated value.
Generating the next value means that the function continues where it left when `yield` was called.

uuid 4db8de3a-1d4b-4fbb-a521-8b25b28667af
anki-guid JF4EKKJ4JV5DORQ=
What are generator expressions?
`generator = (i*i for i in range(a, b))`

uuid c292bdc4-ede1-4adb-8512-6ce53804f4f1
anki-guid J4VEGMCREFKCMYD5
How do you implement an interator class?
To add iterator behaviour to a class,
you define a `__iter__()` method,
which return an object which needs to have a `__next__()` method.
If the class itself has a `__next__()` method,
you can simply define `__iter__()` as the function that returns `self`.

uuid 17313f9e-4894-43fc-b621-9640e5394421
anki-guid OJEDKNLZHZWFWKD4
How do you do multiple inheritance in python?
`class DerivedClassName(Base1, Base2, Base3):`

uuid 763c06db-784a-4c40-9d49-34fa66bef7dd
anki-guid OE7HANBPHVVX2W3R
How do you map a function over a list in python? (Two ways.)
``` python
map(lambda x: x * x, [1, 2, 3])
# or use list comprehension:
[x * x for x in [1, 2, 3]]   
```

uuid ee5780a9-d53a-4eb3-a4c7-7ab330d8cdaf
anki-guid ONMEG4RWIB3HOVJU
How do you filter a list? (Two ways.)
``` python
filter(lambda x: x > 1, [1, 2, 3])
# or use list comprehension:
[x for x in [1, 2, 3] if x > 1] 	
```

uuid 010c6d83-eda3-4068-9dc7-f46d30e9e96e
anki-guid PBLXQ6L2JN4DYOBO
How do you reduce a list in python?
``` python
# import needed in Python 3 only
from functools import reduce

reduce(lambda x, y: x + y, [1, 2, 3], 0)
```

uuid 502f720f-ade7-4f1d-aed6-150a6a3f7443
anki-guid NI5FS3JOFZXDYYSY
How do you do universal and existential test?
```python
all(i % 2 == 0 for i in [1, 2, 3, 4])
any(i % 2 == 0 for i in [1, 2, 3, 4])
```

uuid 46d2156f-a839-48dd-bbdc-45be952c3a4c
anki-guid PJVWG4KGPZRD243E
How do you do variable interpolation in strings?
``` python
count = 3
item = 'ball'
print('{count} {item}s'.format(
  **locals()))
  
# Python 3.6:
print(f'{count} {item}s')
```

uuid 854087e7-126b-49ca-b49e-24e061f5ae5a
anki-guid ORAGUZZKLAYVEORQ
How do you do expression interpolation in strings?
```python
'1 + 1 = {}'.format(1 + 1)

# Python 3.6:
f'1 + 1 = {1 + 1}'
```

uuid 3eefc99e-4361-403b-a26b-5eb52fd23343
anki-guid LU4XCY3JJE7TYVQ=
How do you do string formatting?
```python
'lorem %s %d %f' % ('ipsum', 13, 3.7)

fmt = 'lorem {0} {1} {2}'
fmt.format('ipsum', 13, 3.7)
```

uuid 344304a8-48d8-4fcd-99b5-586315c65b4f
anki-guid MVCH45JNLZWVKTRJ
Format a float.
`f'{math.pi:.{3}}'`

uuid 72d07615-e566-4866-bba9-ae12665005e3
anki-guid NA5F6KT4FB3GI4SI
Convert a number to a string.
`'value: ' + str(8)`

uuid 94a2d88a-18d5-482f-a9c0-2253f8af6d1c
anki-guid OJIFWVRPL5BFQP3S
Join a list of strings.
`' '.join(['do', 're', 'mi', 'fa'])`

uuid 7cfdde0d-1564-4c52-8083-ea117b395379
anki-guid IV6VSSZXGJGXG6LL
Get dict key with default, to avoid KeyError.
`d.get('t', None)`

uuid 93f3a578-1cbb-4edf-8f7d-dd6bff23256e
anki-guid PE5T4K3MPFIX47LS
Check if is key present in a dictionary.
`'y' in d`

uuid ed2efd41-3ee8-4d52-924f-25c06e3bdf62
anki-guid I5UWWVSWFFRSQW2W
Delete an entry of a dictionary.
`d = {1: True, o: False}; del d[1]`

uuid 4fb440ff-c884-4880-bf74-07b665aa6ce4
anki-guid JZIGUT2GJUXXARR3
Merge two dictionaries.
`d1.update(d2)`

uuid 6a456143-e516-413c-88c0-ff5ad6082edb
anki-guid KERVUNKIFNVH2ODI
Iterate over key, value of dictionary.
`for k, v in d.items(): print('value at {} is {}'.format(k, v)`

uuid 8e4bfaa9-d242-4dc0-954c-eb0fe715b150
anki-guid JBVUSM2EM45FG6LL
Dictionary comprehension.
`to_let = {v: k for k, v in to_num.items()}`

uuid 87e27ffe-3bf8-4ab7-9668-3e7e88ded18b
anki-guid IQVFITDVMZMWY2JV
Get keys and values of a dictionary `d` as iterators.
`d.keys(); d.values()`

uuid c0535a67-7999-4ba3-b088-f026718394d9
anki-guid JF7FWU3CGZLV6UDR
Create dictionary from lists.
```python
a = [['a', 1], ['b', 2], ['c', 3]]
d = dict(a)

a = ['a', 1, 'b', 2, 'c', 3]
d = dict(zip(a[::2], a[1::2]))
```

uuid 72d1811d-a2bc-444e-a1a9-dfba7bb8935d
anki-guid MZSXWMJ7HR5H2QTM
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

uuid ba16ec2f-f934-461a-927b-978b59773e01
anki-guid OJRWMT2ZNQUCWUT3
Define a function with private state.
```python
# state not private:
def counter():
  counter.i += 1
  return counter.i

counter.i = 0
print(counter())
```

uuid 0603a7c2-86be-45d0-a4cb-e6bf64907f6c
anki-guid OMSFEZDNMQ2VE4CV
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

uuid aba4af53-2056-4a8b-8dd2-151fff8d406d
anki-guid JVYGKWBGFZSCK5LW
Invoke operators like a function.
```python
import operator

operator.mul(3, 7)

a = ['foo', 'bar', 'baz']
operator.itemgetter(2)(a)
```

uuid 6d463664-6072-4dce-96ec-ce9ad59a9dfb
anki-guid JASDALSBEUTEA4CQ
What do `with`-statements do?
Context management.

uuid 6536ad13-105c-4847-b548-f04e04938baa
anki-guid OA7CY4SKIQXGYQBK
How do you define a context manager?
Make a class with `__enter__()` and `__exit__()`
or use the [`contextlib`](https://docs.python.org/3/library/contextlib.html) library.

uuid 8c70fdd4-3141-4f48-8cc5-0373e7605138
anki-guid NJEEKKBDIQXSUWJU
What does the else clause in a `try ...` statement do?
It is code that is executed when no error has occured.
It is optional.
It is better to place code in the `else` clause then in the `try` part,
to better be able to locate where the error has occurred,
and to not catch the wrong kind of exception.

uuid f68cc9b5-00ec-4d08-b3ae-461759accc7f
anki-guid N4STOYTTOAYSQ5T2
What does the finally clause do in a `try ...` statement?
A *finally clause* is always executed before leaving the try statement, whether an exception has occurred or not. When an exception has occurred in the try clause and has not been handled by an except clause (or it has occurred in an except or else clause), it is re-raised after the finally clause has been executed. The finally clause is also executed “on the way out” when any other clause of the try statement is left via a break, continue or return statement.

uuid 8072dc3f-4cbb-42e7-998b-1ed42a349424
anki-guid IFZU6SDWHMYXG7TC
Raise an exception.
``` python
raise Exception('bad arg') # Here `Exception` is a class.
```

uuid e0a26407-8185-46e9-9e8f-d94096ae2cac
anki-guid MMQSKQCDORCFERLZ
Handle a specific exception.
``` python
try:
  raise Bam()
except Bam as e: # Bam is the class of the exception (defined as `class Bam(Exception): ...`)
  print(e)
```

uuid 749eeefc-89ae-4243-b7eb-48136ce45d74
anki-guid NF6SIO3QGUUW2YKZ
Handle several specific exceptions.
```python
except (RuntimeError, TypeError, NameError):
    pass
```

uuid 64a90dd5-288c-42a9-a0d0-5569f9af12a7
anki-guid NJ5HUJCHFATEAZZ5
Catch-all handler (catch any kind of exception).
``` python
try:
  risky()
except:
  print('risky failed')
```

uuid cb7acc36-29ec-4193-8d7e-c68250e47e33
anki-guid JVNDWWK6FVAC2K2I
Define a new exception.
``` python
class Bam(Exception):
  def __init__(self):
    super(Bam, self).__init__('bam!')
```

uuid cc546fcb-4f34-43af-96ce-e127047b4de2
anki-guid I42F6PJ6JFNDY4SO
How do you get the identity of an object in python? What is it?
`id(obj)`
Every object in python has an identity, a type and a value.
The identity never changes and you can think of it as the object's address in memory.

uuid dd17fbb8-5461-4429-b26f-86710c9cf644
anki-guid OVHUWXK3JE4GEZKB
How do you get the type of an object in python?
`type(obj)`

uuid 5e693481-33e8-413a-bb77-e74ebe0db917
anki-guid PEXWMMRYPZ7GS7S2
How do you define a destructor of a class?
Give it a `__del__` method.

uuid eb2cab6d-27dc-4a78-a669-84f16187ab9b
anki-guid MNOVILTPHJCGY32F
Check that two objects are the same (have the same identities; not just that their values are the same).
Use `is` instead of `==` ( `is` is for identity `==` is for value).

uuid 5de8e3d7-2b85-4663-9ecf-d5fbf2b4ccc8
anki-guid NMZEEI2FFVATYLCA
How do you open a file for reading and writing? To append?
For reading and writing: `open(filename, "r+")`.
For reading and writing if the file possibly does not exist: `open(filename, "r+")`.
For appending: `open(filename, "a")`.

uuid 7b285f17-c838-4c69-b148-9b057d723298
anki-guid PBAEC4JFPVJS2M3Y
How do you read a file and then overwrite it?
```python
with open(filename, "r+") as f:
    data = f.read()
    f.seek(0)
    f.write(output)
    f.truncate()
```

uuid 5f3d0304-4f0e-4c47-a04d-d556a6d57dfa
anki-guid O43TYOZTKFKTKNKF
Turn a value into a boolean.
`bool(val)`

uuid 6e7c50ce-c164-431c-8ea7-c48e476a8bd6
anki-guid JQQSIUBIHRCEENLJ
How do you start to debug a python program?
`python -m pdb programtodebug.py`;
or place a breakpoint in the code:
`import pdb; pdb.set_trace`
or (in python >= 3.7) `breakpoint()`;
or post-mortem: `pdb.pm()`;
or from repl: `pdb.run('mymodule.test()')`.

uuid ff20d6b3-223c-4194-8f5c-376429dca954
anki-guid NIUGWN2UHY3XEU3S
Split an file name into the base name and the file extension.
`os.path.splitext('somefile.ext') => ('somefile', '.ext')`.

uuid d358cddc-1206-4874-b19b-527555be5863
anki-guid PBOTEUBGIY7E2MCL
Get the base name of a file name.
`os.path.basename(filename)`

uuid 502c5402-bc94-4f91-93ae-9aaa0075a41f
anki-guid MROWSQZ3NU6WU7RW
What is the syntax for an `if`-expressions (not `if`-statements)?
`expression_if_true if condition else expression_if_false`

uuid a27601c8-eaa1-4a07-aa4e-0dbdb59ed0a1
anki-guid JZ5CW2T3MVWWKV26
How do you test whether an object/class instance has an attribute? How do you get it (with a default value)?
`hasattr(obj, 'someattribute')`
and
`getattr(obj, 'someattribute', defaultvalue)`

