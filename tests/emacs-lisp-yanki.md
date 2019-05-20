How do you prompt for a string, directory or file name?
With `read-string`, `read-file-name` or `read-directory-name`.
The syntax is usually `(read-string "The prompt that the user is asked")`
and it returns the string that is read.

How do you print a string to the message buffer?
With `(message format-string ...)`.
Note that this accepts the same kind of syntax as `format`,
so you can use `%s` to do string interpolation.

How do you compare whether two strings are equal? Or whether one is smaller than the other?
With `string=` (also: `string-equal`) or `string<`.

How do you convert a string to a char?
With `string-to-char`.

How do you split a string `mystr` at every dash (`-`)?
With `(split-string mystr "-")`.

How do you go to the beginning of a line?
`(goto-char (line-beginning-position))`

How do you go to the beginning of a file?
`(goto-char (point-min))`
