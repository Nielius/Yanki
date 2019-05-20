Ask user for input (name) and store it in an array.
``` C
#include <stdio.h>
int main()
{
    char name[20];
    printf("Enter name: ");
    scanf("%19s", name); 
    /* the number 19 in %19s gives the maximal number of characters to be read;
    since the null character is automatically added, this should be 19. */
    printf("Your name is %s.", name);
    return 0;
}
```
Also, `scanf("%s", name)` stops reading at the first whitespace.
A terminating null character is automatically added.
[scanf op cppref](https://en.cppreference.com/w/cpp/io/c/fscanf)
It seems you can scan until a newline by doing
``` C
char str[100];

scanf("%[^\n]", str);
```

Ask the user to input a number.
``` C
int i;
scanf("%d", &i);
```
Do not forget that you need to give an address!
Otherwise it is of course impossible to store the result.

What is the syntax of `typedef`?
It is exactly like the syntax of a variable declaration,
where the variable name is replaced by the name of the new type.

What is a union?
Like struct, except that the memory of the members overlaps:
you do not have all the members at the same time, you have only one member.

What is an enum? What is the syntax for an enum?
A convenient and structured way to introduce global constants.
Syntax examples:
``` C
enum color { RED, GREEN, BLUE};
enum color r = RED; // OK
// color x = GREEN: // Error: color is not in ordinary name space
typedef enum color color_t;
color_t x = GREEN; // OK

enum { ONE = 1, TWO } e; // enum with identifier for the enum type

enum color {RED, GREEN, BLUE} c = RED, *cp = &c;
 // introduces the type enum color
 // the integer constants RED, GREEN, BLUE 
 // the object c of type enum color
 // the object cp of type pointer to enum color
```

What is tag name space?
It is its own name space.
If you start something with `struct`, `union` or `enum`,
it is looked up in the tag name space.
Other name spaces are `label name space` (for `goto` and `switch`),
member name space (for members of a struct or union)
and the name space of ordinary identifiers.

In what name space do structs, unions and enums live?
Tag name space.

What are the six bit operators? Give the names and symbols.
``` C
A & B; // and
A | B; // or
A ^ B; // xor
~A; // binary complement (flip bits)
A >> 2; // shift 2 to the right
A << 2; // shift 2 to the left
```

What are the normal ways of formatted input and output in C? What header should be included to use them?
`scanf` for input and `printf` for output.
They use similar "placeholders" (such as `%s` and `%c`.)
Include them with `include <stdio.h>`.
To input an entire line, best to use `getline` probably.

What is the difference between `scanf()` and `gets()`?
When they stop reading: `scanf("%s", message)` stops when it encouters a space;
`gets(message)` stops after encountering a newline or EOF.
But note: it may be safer to use `fgets` instead of `gets`,
and `gets` has in fact been removed from `C11`.

What is difference between `fgets` and `gets`?
To prevent buffer overflows, it is probably better to use `fgets`:
it knows about the length of its input and stops reading when it is too long.
This also means that when the input can have arbitrary length,
you have to dynamically allocate longer strings when necessary.
You can also use `getline`, which is perhaps even better.

What is the difference between `fprintf` and `printf`? What do the first and last `f` in `fprintf` stand for?
The first outputs to a general stream; the second outputs to stdout.
The first 'f' stands for "file" (?) and the second for "formatted".

What is the difference between `fscanf` and `scanf`?
The first inputs from a general stream; the second takes input from stdin.

What are the best input and output methods in C?
For input, probably `getline` (but not everywhere supported);
otherwise, `fgets` (which allows you to specify a maximum input length).
You can also use `scanf` (or `fscanf`, if you want to give the stream).

What is the signature of `fgets`? What does it return?
`char * fgets ( char * str, int num, FILE * stream );`
Returns null pointer on failure, and the first argument (`str`) on success.

What is the signature of the main function in a C program? And what are the values?
``` C
int main(int argc, char** argv) {}
```
- `argv[argc]` is a NULL pointer;
- `argv[0]` holds the name of the program;
- `argv[1]` points to the first command line argument.

What does a switch statement look like? How do you give the default option?
``` C
switch(expression) {

   case constant-expression  :
      statement(s);
      break; /* optional */
	
   case constant-expression  :
      statement(s);
      break; /* optional */
  
   /* you can have any number of case statements */
   default : /* Optional */
   statement(s);
}
```

How do you open a file in C? For both reading or writing.
``` C++
// Program beased on FILE handling. 
#include<stdio.h> 
int main() 
{ 
      
    // declaring pointer of FILE type 
    FILE *fp1, *fp2; 
    char c; 
      
    // pointing fp1 to a file geeky.txt 
    // to read from it. 
    fp1 = fopen("geeky.txt", "r"); 
      
    // pointing fp2 to a file outgeeky.txt 
    // to write to it.  
    fp2 = fopen("outgeeky.txt", "w"); 
      
    // reading a character from file. 
    fscanf(fp1, "%c", &c); 
      
    // writing a character to file. 
    fprintf(fp2, "%c", c); 
      
    return 0; 
} 
```

What is the signature of malloc and what does it do? What does it return?
`void* malloc(size_t size);`
--- allocates `size` bytes; returns pointer if succesful.
Allocated bytes need to be freed with `free` or `realloc`.

What function do you use to dynamically allocate memory?
`malloc`

What is the signature of calloc and what does it do? What does it return?
`void* calloc( size_t num, size_t size );`
--- allocates bytes for an array of `num` objects of size `size`.
Sets all bytes to zero.
Return pointer.

What is the signature of ralloc and what does it do? What does it return?
`void *ralloc(void* ptr, size_t new_size)`
--- reallocates (by expanding/contracting, or finding a new area) the given area of memory (given by ptr? how is the size known?
maybe because it has to be constructed with `malloc`, `calloc`, or `realloc`
without having been freed?).
The content of the first (min `new_size` and old_size) bytes remains the same.
Returns pointer to the new memory (or NULL if failed).

What function do you use to expand/contract some memory?
`ralloc`

What is the signature of free and what does it do?
- `void free( void* ptr );`
--- frees the memory pointed to by pointer.
It knows how much memory to erase,
because when you allocate memory with `malloc`,
it includes some data about the size of the memory.
See [this](https://stackoverflow.com/questions/1518711/how-does-free-know-how-much-to-free)
and [this](https://stackoverflow.com/questions/1957099/how-do-free-and-malloc-work-in-c)
for more information.

What is the signature of `memcpy` and what does it do?
- `void * memcpy ( void * destination, const void * source, size_t num );`
--- copies `num` bytes from `source` to `destination`.
Returns `destination`.
(Often, by convention, functions that do not need to return anything, return their first argument,
which allows the following kind of chaining:
`somethirdfunction(somenextfunction(somefunction(arg1, ...), ...), ...)`.)

What is the signature of `memmove` and what does it do?
- `void * memmove ( void * destination, const void * source, size_t num );`
--- like `memcpy`, but as if using an intermediate buffer,
so that there is no problem when `source` and `destination` overlap.

What function would you use to copy a number of bytes from one memory location to another? Which one would you use if the source and destination overlap?
`memcpy`.
When overlapping, use `memmove`, which uses an intermediate buffer
to ensure that overlapping is no problem.

What is the signature of `strcpy` and what does it do?
- `char * strcpy ( char * destination, const char * source );`
--- copy the string `source` to destination, including `\0', but stopping at that.

What is the signature of `strncpy` and what does it do?
- `char * strncpy ( char * destination, const char * source, size_t num );`
--- same as `strcpy`, but copies exactly `num` bytes.
If '\0' is reached before `num` bytes have been copied,
append zeroes.
If '\0' is not yet reached after `num` bytes have been copied,
no '\0' is appended.

What function would you use to copy a string to some destination? What if you want to copy an exact number of bytes?
- `char * strcpy ( char * destination, const char * source );`
--- copy the string `source` to destination, including `\0', but stopping at that.
- `char * strncpy ( char * destination, const char * source, size_t num );`
--- same as `strcpy`, but copies exactly `num` bytes.
If '\0' is reached before `num` bytes have been copied,
append zeroes.
If '\0' is not yet reached after `num` bytes have been copied,
no '\0' is appended.

What is the signature of `strcat` and what does it do?
- `char * strcat ( char * destination, const char * source );`
--- append a copy of `source` to the end of `destination`.
Returns `destination`.

What function would you use to append two strings?
- `char * strcat ( char * destination, const char * source );`
--- append a copy of `source` to the end of `destination`.
Returns `destination`.

What is the signature of `strncat` and what does it do?
- `char * strncat ( char * destination, const char * source, size_t num );`
--- appends first `num` bytes of `source` to `destination`,
plus a termination null-character.

What is the signature of `memcmp` and what does it do?
- `int memcmp ( const void * ptr1, const void * ptr2, size_t num );`
--- compare first `num` bytes of `ptr1` with these of `ptr2`.
Returns 0 if they are equal; otherwise, returns the greater differing value.
Does not care about '\0'.

What is the signature of `memset` and what does it do?
- `void * memset ( void * ptr, int value, size_t num );`
--- sets the first `num` bytes of `ptr` to `value`.
Returns `ptr`.

What is the signature of `strlen` and what does it do?
- `size_t strlen ( const char * str );`
--- gets string length.

How do you get the length of a string?
Using `size_t strlen ( const char * str );`.

