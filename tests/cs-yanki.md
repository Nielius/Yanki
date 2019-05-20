What is copy on write (in computer science)?
Copy-on-write (CoW or COW), sometimes referred to as implicit sharing[1] or shadowing,[2] is a resource-management technique used in computer programming to efficiently implement a "duplicate" or "copy" operation on modifiable resources.[3] If a resource is duplicated but not modified, it is not necessary to create a new resource; the resource can be shared between the copy and the original. Modifications must still create a copy, hence the technique: the copy operation is deferred to the first write. By sharing resources in this way, it is possible to significantly reduce the resource consumption of unmodified copies, while adding a small overhead to resource-modifying operations.

In python, what is the Global Interpreter Lock?
A global interpreter lock (GIL) is a mechanism used in computer-language interpreters to synchronize the execution of threads so that only one native thread can execute at a time.[1] An interpreter that uses GIL always allows exactly one thread to execute at a time, even if run on a multi-core processor. Some popular interpreters that have GIL are CPython and Ruby MRI.

What is big-endian, and what is little-endian?
In big-endian, the most significant byte 
(i.e., the byte that give the greatest potential numerical value)
in a word is stored in the lowest address.
Mnemonic: in big-endian, the bytes are ordered from the big end first.

What is the difference between an identifier and a variable?
A variable is a memory location, where some value is stored.
An identifier is a name for a variable, function, class, structure, ...

What is the difference between a subsequence and a substring?
The difference is that a substring consists of consecutive elements,
whereas a subsequence is as a mathematical subsequence
(there is a monotonically increasing function relating the indices).

