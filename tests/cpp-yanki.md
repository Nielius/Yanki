Compile and run a hello world program.
```C++
$ cat hello.cpp
#include <iostream>

using namespace std;

int main(int argc, char** arg) {
  cout << "Hello, World!" << endl;
}

$ g++ -std=c++0x hello.cpp

$ ./a.out
```

Define a global variable.
```C++
// in foo.cpp and outside of any function
// or class definition:
int foo = 7;

// in bar.cpp and outside of any function
// or class definition:
extern int foo;
```

Find the size of a certain type.
```C++
cout << sizeof(int) << endl;
cout << sizeof(int*) << endl;
```
`sizeof` returns something of type `std::size_t`,
which is an implementation defined type, but probably unsigned int.

Allocate an integer on the heap.
```C++
int* ip = new int;
```

Free an integer from the heap.
```C++
delete i;
```

Null.
```C++
NULL
```

Boolean type.
```C++
bool
```

True and false.
```C++
true false
```

List all integer types and their sizes in bytes.
```C++
signed char n1;   // 1+ bytes
short int n2;     // 2+ bytes
int n3;           // 2+ bytes
long int n4;      // 4+ bytes
long long int n5; // 4+ bytes

unsigned char n1;          // 1+ bytes
unsigned short int n2;     // 2+ bytes
unsigned int n3;           // 2+ bytes
unsigned long int n4;      // 4+ bytes
unsigned long long int n5; // 4+ bytes
```

List all float types.
```C++
float x1;       // 4 bytes
double x2;      // 8 bytes
long double x3; // 16 bytes
```

Make a string in C++ and convert it to C.
```C++
string s("lorem ipsum");

// convert to C string:
const char* s2 = s.c_str();
```

Allocate a string on the heap.
```C++
string* s = new string("hello");
```

Copy a string.
```C++
string s("bar");

// use assignment or copy constructor:
string s2 = s;
string s3(s);

// s contains "baz";
// s2 and s3 contain "bar":
s[2] = 'z';
```

Declare a fixed length array on the stack.
```C++
int a[10];
```

Allocate a fixed length array on the heap.
```C++
int* a = new int[10];
```

Free an array from the heap.
```C++
delete[] a;
```
This is called `operator delete[]`; see this
[reference](http://www\.cplusplus\.com/reference/new/operator%20delete\[]/).

Find the length of an array. Can this be done with every kind of array?
```C++
int a[10];

// stack arrays only: (i.e., only arrays allocated on the stack?)
size_t len = sizeof(a) / sizeof(a[0]);
```

Copy an array to another.
```C++
const size_t LEN(4);
int src[LEN] = {3, 2, 4, 1};
int dest[LEN];

// 3rd arg is number of bytes to copy:
memcpy(dest, src, LEN * sizeof(src[0]));
```

Declare a resizable array.
```C++
#include <vector>

vector <int> a;
```
Note that the elements of a vector always need to be of one type.

Initialize a resizable array.
```C++
#include <vector>

vector<int> a = {1, 2, 3};
// uniform initialization syntax: seems to be the recommended syntax
vector<int> a2 {1, 2, 3};
// vector<int> a3({7, 8, 9}); // does this work?
```

Find the size of a resizable array `a`.
```C++
size_t len = a.size();
```

Slice a vector.
```C++
#include <vector>

vector<int> a({6, 7, 8, 9});

// a2 contains {7, 8}:
vector<int> a2(a.cbegin() + 1,
               a.cbegin() + 3);
```
I think you can also use `begin(a)` and `end(a)`.
According to [the microsoft reference docs](https://docs.microsoft.com/en-us/cpp/standard-library/iterator-functions?view=vs-2019#begin), that is more general,
because it accepts all kinds of containers that do not necessarily have the member function `begin` or `cbegin`.
TODO: there seems to be a difference between `a.begin` and `a.cbegin`,
where the latter is guaranteed to be a `const_iterator`...?
These functions work with all C++ standard library containers.

Slice a vector to the end.
```C++
#include <vector>

vector<int> a({6, 7, 8, 9});

// a2 contains {7, 8, 9}:
vector<int> a2(a.cbegin() + 1, a.cend());
```

How do you push or pop elements to the end of a vector?
```C++
#include <vector>

vector<int> a({6, 7, 8});

a.push_back(9);
int elem = a.pop_back();
```

Manipulate the front of a vector: add and remove elements from the beginning, like push and pop would.
```C++
#include <vector>

vector<int> a({6, 7, 8});

// slower than manipulating back:
a.insert(a.cbegin(), 5);
int elem = a[0];
a.erase(a.cbegin());
```

Concatenate two vectors.
```C++
#include <vector>

vector<int> a1({1, 2, 3});
vector<int> a2({4, 5, 6});

a1.insert(a1.cend(),
          a2.cbegin(),
          a2.cend());

// http://www.cplusplus.com/reference/vector/vector/insert/ 
// You can use the insert command to insert (1) a single element,
// (2) a constant element several times, or
// (3) another vector (or iterator: http://www.cplusplus.com/reference/iterator/InputIterator/)
```

Copy a vector, in two ways.
```C++
#include <vector>

vector<int> a({1, 2, 3});
// copy constructor:
vector<int> a2(a);
vector<int> a3;

// assignment performs copy:
a3 = a;
```

Construct a tuple.
```C++
tuple<string, int, float> tup("foo", 1, 3.7);

// invokes default constructors for elements:
tuple<string, int, float> tup2;

// element types are inferred:
auto tup3 = make_tuple("foo", 1, 3.7);
```

Lookup (= get) elements from a tuple.
```C++
tuple<string, int, float> tup("foo", 1, 3.7);

string s = get<0>(tup);
int i = get<1>(tup);
float x = get<2>(tup);

// type-based access
string s2 = get<string>(tup);
int i2 = get<int>(tup);
float x2 = get<float>(tup);
```

Decompose a tuple.
Pre-C++17:
```C++
tuple<string, int, float> tup("foo", 1, 3.7);
string s;
float x;

tie(s, ignore, x) = tup;
```
With C++17, you can also do:
```C++
tuple<string, int, float> tup("foo", 1, 3.7);
auto [s, someint, x] = tup;
```
and you don't even need to declare the variables before.

Update an an index in a tuple.
```C++
tuple<string, int, float> tup("foo", 1, 3.7);
get<0>(tup) = "bar";
```

Find the length of a tuple.
```C++
tuple<string, int, float> tup("foo", 1, 3.7);
tuple_size<decltype(tup)>::value;
```
Note that `decltype` is a C++11 standard function for getting the declared type.
Some compilers used to implement a `typeof` function, but that was never a standard.
And the class `tuple_type` (which depends on a template) has a static member `value`,
which we access with `tuple_size<decltype(tup)>::value`.

Construct a pair. What do you need to include?
Use `#include <utility>` and:
```C++
pair <string, int> p2("foo", 7);

// invokes default constructors for elements:
pair <string, int> p1;

// element types are inferred:
auto p3 = make_pair("foo", 7);
```

Lookup in a pair.
```C++
auto p = make_pair("foo", 7);

string s = p.first;
int i = p.second;
```

Update in a pair.
```C++
p.first = "bar";
p.second = 8;
```

Construct a dictionary.
```C++
#include <map>

map<string, int> m;
```
If you want unordered map, do:
```C++
#include <unordered_map>

unordered_map<string, int> m;
```

Lookup and update in a dictionary `m`.
```C++
m["hello"] = 5;
cout << m["hello"] << endl;
```

Get the size of a dictionary `m`.
```C++
m.size()
```
See [this overview](http://www.cplusplus.com/reference/map/map/) of all member functions of the map class.

Delete an item of a dictionary.
```C++
std::map<char,int> mymap;
std::map<char,int>::iterator it;
/* ... set values ... */

it=mymap.find('b');
mymap.erase (it); // erasing by iterator
mymap.erase ('c'); // erasing by key
it=mymap.find ('e');
mymap.erase ( it, mymap.end() ); // erasing by range
```
In principle, you can erase by key, by iterator, or by range
(where a range is given using two iterators).
See [this overview](http://www.cplusplus.com/reference/map/map/) of all member functions of the map class.
Note that `std::map` maps are always ordered.
They are [apparently](http://www.cplusplus.com/reference/map/map/) typically implemented as binary search trees
(not as hash tables??).

Explain the missing key behavior in a dictionary.
Returns element created by default constructor of value type.

Define a static class method.
```C++
// Ops.h:
class Ops {
public:
  static int add(int m, int n);
};

// Ops.cpp:
int Ops::add(int m, int n) {
  return m + n;
}
```
Static methods are not bound to a specific instance of the class, but are shared by all
(just as static variables of a class are).
As a result, they do not have a `this` pointer,
and can not access non-static member (variables or functions).
They can be accessed through the class as well using `Ops::add`,
without having even defined an instance.

Overload a function `add`.
```C++
int add(int m, int n) {
  return m + n;
}

float add(float x, float y) {
  return x + y;
}
```

Specifiy default arguments.
```C++
#include <cmath>

float
logarithm(float x, float base = 10.0) {
  return log(x) / log(base);
}
```

Pass an argument by reference.
```C++
int add1(int& n) {
  return ++n;
}

int i(7);

// set i and i2 to 8:
int i2 = add1(i);
```

Pass by address.
```C++
int add1(int* n) {
  return ++*n;
}

int i(7);

// set i and i2 to 8:
int i2 = add1(&i);
```

Create an anonymous function and store it in an identifier. What does the first part of an anonymous function mean?
```C++
auto add = [](int n, int m) {
  return n + m;
};
```
The `[]` in `[](int n, int m)` is the capture clause,
and you can give it all kinds of options to specify which of the variables in the environment
are captured in the anonymous functions.
For example, with `[&]` all variables in the body are captured by reference.
Also see [microsoft's explanation](https://docs.microsoft.com/en-us/cpp/cpp/lambda-expressions-in-cpp?view=vs-2019).

Invoke an anonymous function `add` of two integer arguments.
```C++
//on variable holding anon. function:
int sum = add(3, 7);

// on lambda expression:
int sum2 = [](int n, int m) {
  return n + m;
}(3, 7);
```

Define a function with private state.
```C++
int counter() {
  static int i = 0;
  return ++i;
}
```

Overload the operator `+` for rational numbers (`Rational`).
```C++
Rational Rational::operator+(Rational& o) {
  return Rational(this->num * o.denom + o.num * this->denom, this->denom * o.denom);
}
```

If and else if.
```C++
int signum;

if (n > 0) {
  signum = 1;
}
else if (n == 0) {
  signum = 0;
}
else {
  signum = -1;
}
```

Switch.
```C++
const int INVALID_BINARY_DIGIT(-1);
int bin_digit;

switch(n) {
case 0:
case 1:
  bin_digit = n;
  break;
default:
  bin_digit = INVALID_BINARY_DIGIT;
  break;
}
```

Break out of a nested leap.
```C++
int data[2][2] = {{3, 2}, {0, 1}};
int i, j;
bool has_zero(false);

for (i = 0; i < 2; ++i) {
  for (j = 0; j < 2; ++j) {
    if (data[i][j] == 0) {
      has_zero = true;
      goto end_of_loops;
    }
  }
}
:end_of_loops
```

Continue in a loop.
```C++
int a[4] = {3, 2, 0, 1};

for (int i = 0; i < 4; ++i) {
  if (a[i] == 0) {
    continue;
  }
  cout << 1.0 / a[i] << endl;
}
```

Raise an exception.
```C++
#include <cstdlib>
#include <stdexcept>

void risky() {
  if (rand() < 10) {
    throw runtime_error("bam!");
  }
}
```
You can also just throw an int or string:
`throw "Division by zero condition!";`
or `throw 20;`.
The latter can be caught with `catch(int n)`, for example,
and `n` will be 20.

Handle an exception.
```C++
#include <stdexcept>

try {
  risky();
}
catch (const exception &e) {
  cout << e.what() << endl;
}
```
Note that `what()` is a method (actually the only useful method)
of the class `std::exception`;
it returns an explanatory string.
(See [cppreference on the exception class](https://en.cppreference.com/w/cpp/error/exception).)
--- Another example:
``` C++
// exceptions
#include <iostream>
using namespace std;

int main () {
  try
  {
    throw 20;
  }
  catch (int e)
  {
    cout << "An exception occurred. Exception Nr. " << e << '\n';
  }
  return 0;
}
```
You can throw basically everything;
see [cppreference on the throw statement](https://en.cppreference.com/w/cpp/language/throw).

Define a new exception.
```C++
#include <stdexcept>

class Bam : public runtime_error {
public:
  Bam() : runtime_error("bam!") {}
};

throw Bam();
```

Re-raise an exception after catching it.
```C++
#include <stdexcept>

try {
  risky();
}
catch (const exception& e) {
  cout << "an error occurred..." << endl;
  throw;
}
```

Catch-all handler.
```C++
#include <stdexcept>

try {
  risky();
}
catch (...) {
  cout << "an error was ignored"
       << endl;
}
```
Note that `...` is an actual ellipsis;
as far as I know, this is not a specific case of more general syntax.

Handle multiple kinds of exceptions.
```C++
#include <stdexcept>

try {
  risky();
}
catch (const system_error &e) {
  cout << "system error: " << e.name()
       << endl;
}
catch (const exception &e) {
  cout << "exception: " << e.what()
       << endl;
}
catch (...) {
  cout << "unknown error" << endl;
}
```

List the standard file handles.
cin cout cerr clog
To use them, you have to include `<iostream>`:

What should the standard preamble look like?
``` C++
#include <iostream>
using namespace std; // allows you to write e.g. cin instead of std::cin
```

Read a line from stdin.
```C++
string s;
cin >> s;
```

Write a formatted string to stdout.
```C++
cout << "count: " << 7 << endl;
```

Read from a file.
```C++
#include <fstream>

string line;
ifstream f("/etc/passwd");

if (f.is_open()) {
while (!f.eof()) {
    getline(f, line);
    // process line
  }
  f.close();
  if ( 0 != f.fail() ) {
    // handle error
  }
}
else {
  // handle error
}
```
Some examples from [cplusplus.com](http://www.cplusplus.com/doc/tutorial/files/):
``` C++
// writing on a text file
#include <iostream>
#include <fstream>
using namespace std;

int main () {
// Read from a file:
  string line;
  ifstream myfile ("example.txt");
  if (myfile.is_open())
  {
    while ( getline (myfile,line) )
    {
      cout << line << '\n';
    }
    myfile.close();
  }

else cout << "Unable to open file";
// open a file in read mode.
   ifstream infile; 
   infile.open("afile.dat"); 
 
   cout << "Reading from the file" << endl; 
   infile >> data;

// Writing to a file:
ofstream myfile ("example.txt");
  if (myfile.is_open())
  {
    myfile << "This is a line.\n";
    myfile << "This is another line.\n";
    myfile.close();
  }
  else cout << "Unable to open file";
  
  
 
  / 
  
  return 0;
}
```

Write to a file
```C++
#include <fstream>

ofstream f("/tmp/test4");
int i;

for (i = 0; i < 10; ++i) {
f << i << endl;
}
f.close();
if (0 != f.fail()) {
  // handle error
}
```

State the signature of the `main` function.
```C++
int main(int argc, char** argv) {
```

Declare a namespace.
```C++
namespace foo {
  namespace bar {
    class Baz {
      static const int ANSWER = 42;
    };
  }
}
```

Import a namespace.
```C++
using namespace foo::bar;
```
And when the namespace is declared like this:
```C++
namespace foo {
  namespace bar {
    class Baz {
      static const int ANSWER = 42;
    };
  }
}
```
then you can use it as
```
cout << Baz::ANSWER << endl;
// (This is given a class Baz inside a namespace bar inside a namespace foo)
```

What is virtual inheritance?
By placing the `virtual` keyword in front of the base class name in an inheritance,
you ensure that the base class is inherited only once.
(In multiple inheritance,
1the "diamond problem" is the phenomenon
where a derived class derives from two bases classes,
both of which in turn derive from another single base class.
The most derived class then inherits the top most base class twice:
once through each direct base class.)

Suppose a class `Manager` derives from the class `Employee` and you want to implement the `Manager`'s `print` function in terms of the print function of `Employee`. How do you call the `print` function of `Employee` from within the `Manager` class?
Using `Employee::print()`.

What is a virtual method of a class?
Member functions of a class can be specified as `virtual` to solve the following problem.
Suppose that you have a pointer of type `BaseClass*`,
but the object pointed to is in fact an instance of a class `DerivedClass` derived from `BaseClass`.
If you then call a method of this pointer,
should this refer to the method defined in `BaseClass` or the method defined in `DerivedClass`?
By specifying a function as `virtual`,
you signal that the method from the derived class should be called,
which allows you to redefine the function for every derived class.
(See §12.2.5 in Stroustrup's C++ the language.)

Use the constructor of a superclass to define the constructor of the derived class.
The syntax for this situation is as if the base class is just any other member of the derived class, i.e., using a [member initializer list](https://en.cppreference.com/w/cpp/language/initializer_list ) for the constructor.
```C++
Integer::Integer(int n) : Rational(n, 1) {
}
```

Get the type class from a type identifier.
```C++
#include <typeinfo>
typeid(Foo) // object of type const std::type_info
```
Note that these objects of `type_info` can be equality-compared,
but otherwise do not really contain any useful methods (at least in the standard):
it has a method `name()`, but that is not guaranteed to produce anything legible.
See for example [this SO explanation](https://stackoverflow.com/a/1986485)
or [this reference](https://en.cppreference.com/w/cpp/language/typeid)
N.B.: `typeof` is used in some compiler extensions, but is not part of C++; use `decltype`.

Get a class name from a type identifier.
```C++
 	typeid(Foo).name()
```

Store an adress in a pointer and then dereference the pointer.
```C++
int i = 5;
int* ptr = &i;
int i2 = *ptr;
```

List all the bit operators and their syntax.
```C++
`<< >> & | ^ ~ `
```
e.g.
``` C
A & B; // and
A | B; // or
A ^ B; // xor
~A; // binary complement (flip bits)
A >> 2; // shift 2 to the right
A << 2; // shift 2 to the left
```

What do the `const` and `volatile` type qualifiers do?
Const specifies that the object cannot be modified.
A direct attempt to modify it is a compile-time error;
indirect modifications (through e.g. pointers or references)
are unspecified.
Volatile ensures that variables are not stored in registers,
but always accessed from memory.
This is useful when other programs/threads (?)
can modify the memory.

What does the keyword `static` do for (1) a variable in a function; (2) a global variable or function definition; (3) a class member?
For (1) and (3), it is defined only once, shared by all instances. The line that defines it (gives it a value) is skipped the next time it is encountered. This changes the duration.
In case (3), if a member function is static, then it does not have a `this` pointer. You can use it if the function does not depend on the instance of the class.
For (2), the linkage is changed: it now internally linked and can therefore only be accessed
from within the translation unit.

What does the keyword `extern` do?
Changes the duration and linkage of global variables: they are now statically defined
and externally linked.

What does external or internal linkage mean?
A name that can be used in translation units different from the one in which it was defined,
it said to be externally linked.
If a name can only be used in the translation unit in which it is defined,
it is internally linked.
The keyword `static` was used in C and older C++ programs to denote internal linkage.
Strousup recommends only to use `static` in functions and classes.
There are sane defaults for internal/external linkage; see [cppreference.com](https://en.cppreference.com/w/cpp/language/storage_duration).

What is automatic, static, thread-local (C++11) or dynamic storage duration?
Say when storage for an object is allocated and de-allocated.
Summary --- automatic: from beginning to end of code block;
static: from beginning to end of program;
thread: from beginning to end of thread;
dynamic: programmer has to manually specify.
Automatic storage duration --- The storage for the object is allocated at the beginning of the enclosing code block and deallocated at the end. All local objects have this storage duration, except those declared static, extern or thread_local. 
Static storage duration --- The storage for the object is allocated when the program begins and deallocated when the program ends. Only one instance of the object exists. All objects declared at namespace scope (including global namespace) have this storage duration, plus those declared with static or extern. 
Thread storage duration (since C++11) --- The storage for the object is allocated when the thread begins and deallocated when the thread ends. Each thread has its own instance of the object. Only objects declared thread_local have this storage duration. thread_local can appear together with static or extern to adjust linkage. See Non-local variables for details on initialization of objects with this storage duration. 
Dynamic storage duration --- The storage for the object is allocated and deallocated per request by using dynamic memory allocation functions. See new-expression for details on initialization of objects with this storage duration.
([source](https://en.cppreference.com/w/cpp/language/storage_duration))

Why does `cout` work as it does?
It is an object, which has an implementation for the insertion operator `<<`.
This insertion operator returns (a reference to) `cout` again, so that you can chain the results.
This is similar to chaining methods of an object `obj` by writing
`obj.method1().method2().method3()`
where each of the methods returns (a reference to) an object that implements the next method.

What is an inline function?
If a function is inline, then the compiler replaces function calls by the code that defines the function.

Give an example of a scoped enum.
``` C++
enum class Days {Saturday, Sunday, Tuesday, Wednesday, Thursday, Friday};
Days day = Days::Saturday;
if (day == Days::Saturday)
```

What does `const` mean after a member function declaration, e.g. `type CLASS::FUNCTION(int, const char*) const` in a class?
It means that this function does not modify the observable state of the calling instance
(except for members that are declared to be `mutable`).
In compiler terms, it means that you cannot call a function on a const object (or const reference or const pointer) unless that function is also declared to be const. Also, methods which are declared const are not allowed to call methods which are not.

What does the `public|protected|private` in an inheritance mean?
In an inheritance situation, we mean by "derived class"
the class that inherits from the other class,
which we call the "base class".
The access specifier `public|protected|private`
means that all the members of the base class
that the derived class inherits, are assigned an access specifier
that is at most as accessible as the given access specifier.
In other words, if you specify `public`,
then all members of the base class keep their access specification;
if you inherit with `private`, then all members of the base class become
`private` in the derived class.

If `public|protected|private` is missing from an inheritance statement, what is the default?
For classes, the default is `private`; for structs, `public`.
See [this link](https://en.cppreference.com/w/cpp/language/derived_class).

Define a subclass `Integer` of the class `Rational`.
```C++
class Integer : public Rational {
 public:
  Integer(int n);
  virtual ~Integer();
};
```

How do you declare a function with a template?
``` c++
template <class identifier> function_declaration;
template <typename identifier> function_declaration;
```
Both expressions have the same meaning and behave in exactly the same way. The latter form was introduced to avoid confusion, since a type parameter need not be a class. (It can also be a basic type such as int or double.)

How do you reverse a vector?
To change the vector in-place, use `std::reverse` from `#include <algorithm>`.
This changes the vector in-place:
``` c++
#include <vector>
#include <algorithm>

int main() {
  std::vector<int> a;
  std::reverse(a.begin(), a.end());
  return 0;
}
```
If you want an iterator that goes in the reverse direction,
you can use `vector::rbegin()` and `vector::rend()`,
which are so-called "reverse iterators", which iterate backwords:
increasing them moves them towards the beginning of the container.

What is a reverse iterator? How do you turn a normal (bidirectional) iterator into a reverse iterator?
A reverse iterator is one where the increment operation actually lowers the iterator.
You can turn a normal iterator into a reverse iterator with `make_reverse_iteror(someiterator)`;
For example, you can use this in the following example:
``` c++
auto it = make_reverse_iterator(a.end());
while (it != make_reverse_iterator(a.begin())) {
   cout << *it << ", ";
   it++;
}
```
although here it would have been easier to loop over `a.rend()` and `a.rbegin()`,
which are the reverse iterators that we need.

How do you sort a vector (or any container with iterators)? In what order does it sort?
Using `sort(begin_iterator, end_iterator[, Compare comp_function])`
from `algorithm`.
This sorts in ascending order.
`comp_function` should be a function of two arguments returning a bool, which is true if
the first element should go before the second argument.
In the `function` library, there is a function `greater<int>` that you can use to change the order;
see <http://www.cplusplus.com/reference/functional/greater/>

How do you raise a number to a certain power?
Using `pow` from `cmath`.

How do you get the length of a string `string s`?
With `s.length()` or `s.size()`.
They are synonyms.
(declaration: `size_t string::length() const`)

Can you have nested functions in C++?
No, but in modern versions of C++, you can use lambdas,
which have sort of the same effect
(and can also capture variables in the environment).
See [this question](https://stackoverflow.com/questions/4324763/can-we-have-functions-inside-functions-in-c).

How do you convert a string to an integer? And an integer to a string?
With `stoi` from `string` and `to_string`.

What is a `bitset`? In what package is it? What are some functions? How do you declare a bitset of a certain length?
A `bitset` (from the package `bitset`) is like an array of `bool`s,
but optimized for space allocation.
You can reference elements as you could in an array.
You can set bits with `set` (to 1), `reset` (to zero) or `flip`
(all taking one argument: the position `size_t pos`);
there are `any` , `none `and `all` functions.
With `test(size_t pos)` you check if position `pos` is set.
http://www.cplusplus.com/reference/bitset/bitset/
``` c++
#include <bitset>         // std::bitset

std::bitset<16> foo; // 16 zeroes
std::bitset<16> bar (0xfa2);
std::bitset<16> baz (std::string("0101111001"));

foo[2] = 1;
cout << foo.size(); // returns 16
```

How do you add some text to the end of a string `mystr`?
With `mystr.append("some text")`.
Note that you can also specify a range (with iterators).
See [cplusplus.com](http://www.cplusplus.com/reference/string/string/append/).

How do you get all combinations of `r` elements out of a certain vector using (mostly) standard library functions?
Use the fact that you can get permutations
and use a "mask" (i.e., a vector of bools) that consists of `r` trues and `n - r` falses.
It then looks something like this:
``` c++
std::vector<bool> v(n);
std::fill(v.begin(), v.begin() + r, true);

do {
  for (int i = 0; i < n; ++i) {
     if (v[i]) {
        std::cout << (i + 1) << " ";
     }
}
std::cout << "\n";
} while (std::prev_permutation(v.begin(), v.end()));
```
[Source](https://stackoverflow.com/a/9430993)

How does `std::next_permutation` from `algorithm` work? What is the input? What does it do? What does it return?
- Input: a range (given as two bidirectional iterators)
and optionally a comparison function.
- Side-effect: permutes the elements to give the *next* lexicographically larger
permutation.
    - Note that, if every element in the range can be compared to every other element,
    this induced a lexicographical order on vectors of those elements.
    This order orders the permutations, so it makes sense to speak of the "next".
    - If this is already the largest permutation, return the smallest permutation.
- Return value: true, unless the starting permutation was the largest possible permutation.

