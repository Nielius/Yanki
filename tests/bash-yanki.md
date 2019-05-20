Rapidly invoke an editor to write a long, complex, or tricky command.
- `fc` (and starts with a previous command; short for 'fix command')
- `C-x C-e` in emacs mode or `esc v` in vim mode (`set -o -vi`); this edits the current command

How do you substitute a pattern by a string in a paramter?
`${parameter/patterng/string}`

How do you remove a matching prefix pattern from a parameter?
`${parameter#word}` to remove the shortest matching pattern,
`${parameter##word}` to remove the longest matching pattern.

How do you remove a matching suffix pattern from a parameter?
`${parameter%word}` to remove the shortest matching pattern,
`${parameter%%word}` to remove the longest matching pattern,

Write a for loop
```bash
for VAR in ARG
do
  CMD
  ...
done
```

Write an if, else if, else statement
```bash
if test
then
  cmd
  …
elif test
then
  cmd
  …
else
  cmd
  …
fi
```

In Bash, what are the differences between single quotes ('') and double quotes ("")?
Single quotes don't interpolate anything (not variables, backticks, `\` escapes),
while double quotes do.

What is the special variable `$#`?
The number of arguments (without counting the script name variable `$0`).

How do you tell xargs to replace a certain string with the input?
`xargs -I{}` for `{}`

How do you tell `xargs` to change the delimiter?
With the `-d` flag.

How do you tell `xargs` to expect that the items are terminated by the null character?
Using `-0` or `--null`.

How do you tell `find` to separate items with the null character? How is this useful?
With `-print0`. Useful in combination with `xargs` for files that contain spaces.

What is the `-r` flag in `read -r`?
It says not to interpret backslashes as escape characters.
I think it stands for "raw".

What is a read-while loop in bash?
It looks like:
```bash
while read -r varname;
do
   bladiebla
done
```
It processes the stdin by reading it one line at a time and saving the line in the variable
`$varname`.

What is process substitution? What is the syntax? The syntax is something like
`diff <(process for one file) <(process for another file)`.
The process list is run asynchronously, and its input or output appears as a
filename. This filename is passed as an argument to the current command as the
result of the expansion. If the `>(list)` form is used, writing to the file
(i.e., the file name that is put in the place of `>(list)`) will
provide input for `list`. If the `<(list)` form is used, the file passed as an
argument should be read to obtain the output of `list`. Note that no space may
appear between the `<` or `>` and the left parenthesis, otherwise the construct
would be interpreted as a redirection. Process substitution is supported on
systems that support named pipes (FIFOs) or the /dev/fd method of naming open
files.
[Source](https://www.gnu.org/software/bash/manual/bash.html#Process-Substitution)

Given a filename, how do you get the part that excludes the directory?
With `basename filename`.

Given a filename, how do you get the directory it is in?
With `dirname`. Possibly you could also do something like `${filename%/*}`
to remove the suffix.

In bash, given a directory variable `$DIRVAR` that possibly ends in `/`, but possibly not, how do you join the directory with a filename `$FILENAME`?
The POSIX standard mandates that multiple consecutive `/` are treated as a single `/`, so you can simply do
`fullpath="${DIRVAR}/${FILENAME}"`.

What does a bash here-doc look like?
``` bash
$ sed 's|http://||' <<EOL
http://url1.com
http://url2.com
http://url3.com
EOL
```

How do you make file descriptor 6 a copy of (or better: point to the same as) file descriptor 7, without executing a comand?
With `exec 6>&7`.
I think the `&` is necessary to distinguish this from
"redirect file descriptor 6 to the file that is named '7'".

How do you open a custom file descriptor? How do you close it?
``` bash
exec 3<> file                # Open a file for reading and writing using a custom file descriptor.
exec 3>&-                    # Close a file descriptor.
```

What is a safe way to get the directory that a script is run in?
`DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"`
If you only need to go to the directory, you can just do
`cd "$( dirname "${BASH_SOURCE[0]}" )"`.
(Apparently, this may fail when `CDPATHS` is set.)

What does the shift command do?
It sets `$1` equal to `$2`, `$2` to `$3`, etc.
The special positional parameter `$0`
is left untouched.

If you're making a symbolic link with `ln -s`, what is the first argument and what is the second?
First is target of the link, second is the link name.
Think of it like a `cp` or `mv `operation.

Given a relative path `$relpat` in a shell script, how do you get the full path and follow symlinks?
With `readlink -f $relpat`.

Define an array.
`somearray=( "val1" "val2" .... "valn" )`

Loop over the elements in an array.
`for elem in "${files[@]}"`
Note that the difference between "${files[@]}"
and "${files[*]}" appears here:
If the word is double-quoted, `${name[*]}` expands to a single word with the value of each
array member separated by the first character of the IFS special variable, and
`${name[@]}` expands each element of name to a separate word.

What does `git reflog` do?
One of the things Git does in the background while you’re working away is keep a reflog — a log of where your HEAD and branch references have been for the last few months.
The reflog is an ordered list of the commits that HEAD has pointed to: it's undo history for your repo. The reflog isn't part of the repo itself (it's stored separately to the commits themselves) and isn't included in pushes, fetches or clones; it's purely local.
[Source](https://stackoverflow.com/questions/17857723/whats-the-difference-between-git-reflog-and-log).

With grep, how do you ensure that the filename is printed?
With `-H`.

With grep, how do you do a recursive search?
With `-r` or (if you want to follow all symlinks) `-R`.

What should you do instead of `cat onlyOneFile | somecommand`?
You can simply do `< onlyOneFile somecommand`.
This was a [useless use of cat](http://www.catb.org/jargon/html/U/UUOC.html).

With `xargs`, how do you apply multiply commands per argument?
By using `sh -c ' command1; command2; ....'`,
e.g. `< a.txt xargs -I % sh -c 'command1; command2; ...'`.

How do you define a function in bash?
There are two ways:
with `function functionname { ... }`
or with `functionname () { ... }`,
so either with the keyword `function` or with `()` after the name.
Note that there are not really "variables" or return values:
you can only return exit codes
and you access the arguments with e.g. `$1`.
As an example:
```bash
#!/bin/bash 
function quit {
exit
}  
function e {
   echo $1 
}  
e Hello
e World
quit
echo foo 
```

What is the syntax for a heredoc?
```bash
interactive-program <<LimitString
command #1
command #2
...
LimitString
```

How do you make sure that `echo` interprets backslash escape sequences?
By passing the `-e` flag (for enable).

Name two ways to group commands. What is the difference? Why would you do that?
You can group commands with either `( list )` or `{ list; }`.
The first creates a subshell, while the second doesn't.
Note that with curly braces, the list has to be termined with `;`.
(Also, the curly braces have to be separated by whitespace, because they are "reserved words", whereas the parentheses are operators and do not.)
You might want to do such a thing,
because you want to pipe the output of multiple commands.

How do you specify a range of integers (from 0 to 10, say) with some skipping step (of e.g. 2)? Or a range of letters?
With curly braces and double dots:
```bash
echo {0..10}
echo {10..0}
echo {10..0..2}
echo {z..a..2}
echo {a..z}{a..z} # outputs all combinations
```
(As the last example shows, you can even combine them!)
