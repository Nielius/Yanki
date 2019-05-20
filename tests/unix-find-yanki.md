Using find, specify to search for a certain filename.
`find . -name "*.jpg"`
Note that this is not a regular expression, but more like bash expansion.

Using find, specify to search for a certain filename case insensitively.
`find . -iname "*.jpg"`
Note that this is not a regular expression, but more like bash expansion.

Using `find`, specify to search for files or directories.
`find . -type d` for directories and
`find . -type f` for files.

Using find, search for files that were accessed (resp. changed, modified) n minutes (resp. days) ago.
For access: use `amin` and `atime`;
for changed, use `cmin` and `ctime`;
for modified, use `mmin`, and `mtime`.
The `time`-flags search for days, the other for minutes.

Using find, search for a file path that matches a regular expression.
Using `-regex pattern`, you can try to match the whole path.
The kind of regular expressions it understands are Emacs Regular Expressions,
but this can be changed with `-regextype`.

Using find, how do you specifiy that a numerical value should be at least, at most or exactly `n``?
With `+n`, `-n` or `n`.

Using find, delete the files that are found.
Add `-delete` at the end.

Using find, execute some custom action on the files that are found. How do you put the filename of the found file in the command?
It is best to use `-execdir command ;`.
You could also use `-exec` instead of `-execdir`,
but `-execdir` is safer:
it runs from the directory in which the file is found
and apparently avoids race conditions.
Any occurence of `{}` is replaced by the filename.
You can also use `-execdir command {} +`
(only one occurence of `{}` allowed) to append each found file at the end of the list.
NOTE: many things need to be escaped in shell, such as `;`: you should use `\;` in bash.

Using find, just print the filenames.
`-print`.

Using find, print the filenames, separated by a null character.
`-print0`.

Using find, print using a special format.
`-printf`.

Using find, delete all files with a certain extension.
E.g., to find files with extension '.txt' and remove them:
`find ./path/ -name '*.txt' -exec rm '{}' \;`

To find files with extension '.txt' and look for a string into them:
`find ./path/ -name '*.txt' | xargs grep 'string'`

Using grep, find files with a size bigger than 5 MB (resp. kb, resp GB).
`find . -size +5M -type f -print0 | xargs -0 ls -Ssh | sort -z`
For kilobye, use `k`; for gigabyte, use `G`.

How can you let find execute a shell command that bash should not yet substitute? For example, you would like to do `-exec cp {} $(basename {})`. Why does that not work? What can you do instead?
The example doesn't work, because the substitution `$(basename {})` is done before executing the `find` command.
You can solve this by using `-exec sh -c 'cp {} $(basename {})'`,
because in single brackets, nothing is expanded.

