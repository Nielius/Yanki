Caution: This is still a work in progress and though all functionality is there,
the user should be careful and prepared to run into some bugs.
Setting it up probably requires some fiddling.
It is a command-line program and does not have a GUI.
Use at your own risk.

With Yanki (originally short for Yaml + Anki),
you can store your Anki (a flashcard program)
cards in very easy-to-read plain text files
(either YAML or Markdown).
You can write these files in your favorite text editor
and use Yanki to import them to Anki.
Any future changes to the notes can be made in the same file,
and by running Yanki again, you can update the corresponding notes in the Anki database.
Additionally, you can use
using [Jinja templates](http://jinja.pocoo.org/)
to export your cards to any other format.

Why is this useful? It allows you to:

- write notes in your favorite text editor and import them into Anki or export them to any other format;
- put your notes under version control;
- easily share your notes without excessive metadata;
- search through your notes;
- write your own programs or scripts to create or process the cards; and
- store your notes forever: plain text files will always be there.

The exporting functionality is based on [Jinja templates](http://jinja.pocoo.org/).
You can build your own templates or you can use and modify the example templates in ????.
I find this especially useful for learning cards for the first time:
if I'm learning a new topic for which I already have cards,
I want to be able to see the connections between the cards,
repeat them a few times
and correct any mistakes, for example.

TODO: point people to examples

# Examples

# Installation

Clone the github repository. The main program is `bin/yanki.py`, so you may want to create a symlink to that file in one of your directories in your path.

In addition to that, you need the [Anki source code](https://github.com/dae/anki),
which is used to access the Anki databases.
You can either specify the path to the anki  source in the configuration file
(see [Configuration](#Configuration)),
make a symlink `YANKIPATH/bin/anki` to the folder with the Anki source code,
or put the Anki source somewhere where Python can find it.


# Configuration

Whenever it is run,
Yanki takes its arguments from three sources:

- the command line arguments;
- the metadata associated to the Yanki file; and
- the default configuration in `~/.yanki.yml` or `~/.local/share/Yanki/config.yml`,
which should be a Yaml dictionary.

The earlier source in this list takes precedence over the sources that follow it.

As of now, there are only a few things you can configure in `~/.yanki.yml`:

- the path to the default Anki collection
(usually something like `~/.local/share/Anki2/User 1/collection.anki2`).
stored in the `collection` variable;

- the path to the Anki source code
stored in the `ankisource` variable;

- the directories in which Yanki should look for templates,
in addition to the `templates` directory in the Yanki directory.
This can be stored in the variable `templateDirs`
as a list of strings.

For example, the configuration file could look like this:

```
ankisource: "/path/to/anki/source/anki"
collection: "~/.local/share/Anki2/Tmpuser/collection.anki2"
templateDirs: ['~/mytemplates', '~/more/templates']
```

# File formats

The notes are stored in what I call Yanki files.
These are Markdown or Yaml files that follow the following conventions.

## Markdown

When importing notes written in a markdown file, the Yanki parser assumes that the markdown files is structured as follows:

- empty lines separate notes (except for empty lines within markdown code blocks);
- the first line of every note that does not start with `uuid` or `anki-guid` is the question; and
- the answer is composed of all lines following the question.

Optionally, two lines starting with `uuid` and `anki-guid` respectively precede the question line.

## Yaml

The Yaml files are structured as follows.
The strings are interpreted as strings with markdown formatting.
The file itself is a list of dictionaries,
where each dictionary has at least the fields `question` and `answer`.
When the first dictionary has a field `metadata` with the value `true`,
then it is interpreted not as a note with a question and an answer,
but as a dictionary that provides some of the associated metadata,
as explained in the next subsection.

This format is potentially more expressive,
but is correspondingly less comfortable to type.
In the future, Yanki may be able to use this extra expressiveness.


## Metadata

Both markdown and Yaml Yanki files can contain metadata.
At the moment, this metadata is only used to determine
the path of the Anki database
(usually something like `~/.local/share/Anki2/User 1/collection.anki2`)
and the name of the deck to which notes should be saved.
This metadata is stored in a different way in markdown Yanki files than in Yaml Yanki files.

In markdown Yanki files,
the metadata is stored in a "buddy file" (or "sidecar file"),
which is a file with the same name as the Yanki file, but with `.yml` appended.
This is a yaml file that contains precisely one dictionary,
with the keywords `collection` (for the path to the collection)
and `deck` (for the name of the deck).

In Yaml Yanki files,
the metadata is stored in the file itself:
it is the first dictionary in the list of dictionaries that otherwise only consists of notes.
This first dictionary should contain the field `metadata` with value `true`
and is otherwise the same as the dictionary describing the metadata for markdown Yanki files.

If the metadata dictionary contains any other fields,
they are ignored.
If the deck name is not given in the metadata,
Yanki takes the filename of the Yanki file without the extension as the name for the deck.


## The uuid and anki-guid fields

When Yanki imports a Yanki file, it supplies every note with a uuid and an anki-guid field.
In the Markdown format, these are given by two lines before the question, and in the Yaml format,
they have their own fields in the dictionary.
The `uuid` is made with Python's `uuid.uuid4` function and does not play any role yet
(but it is supplied as an extra field in the imported notes),
but is implemented as a safety feature and may serve some future purpose.
The `anki-guid` is a base 32 encoding of the guid that Anki generates for each note.
This is used to update the note in Anki's database when the note in the Yanki file changes.



# Usage

- for command line options, use `yanki --help`

# Disadvantages

Yanki is *less expressive* than Anki itself ---
The easy format comes at a price:
not all of Anki's advanced features are available.
For example, with the markdown format,
you can only provide two fields (a question and an aswer),
and you can use only one model (= note type).
The YAML format offers more expressiveness,
but still not as much as Anki itself.
However, for many purposes, I find I don't really need all Anki's advanced formatting options
and a simple question/answer note suffices.

Yanki is still quite *immature*  ---
expect back-ups and assume that your Anki database and your Yanki files may not survive the process.
So far I've had no such problems, but I would not risk losing any important data.

# Related projects

These are related projects that I'm aware of. Please let me know if you of others!

- [crowdAnki](https://github.com/Stvad/CrowdAnki)
--- similar, but uses very elaborate JSON files that you would not want to write on your own.
- Anki itself has some export features 
- [AnkiConnect](https://github.com/FooSoft/anki-connect)
([plugin on AnkiWeb](https://ankiweb.net/shared/info/2055492159))
--- RESTful API for Anki features
- [ankisync](https://github.com/patarapolw/ankisync)
--- extending AnkiConnect
- [anki-cli-remote](https://github.com/glutanimate/anki-cli-remote)
--- command-line interface for Anki, based on AnkiConnect
- [Clanki](https://github.com/marcusbuffett/Clanki)
--- command-line spaced repetition system (stand-alone program independent of Anki)
- [genanki](https://github.com/kerrickstaley/genanki)
--- a library for generating Anki decks
- [LaTeX Note Importer for Anki](https://tentativeconvert.github.io/LaTeX-Note-Importer-for-Anki/)
([github](https://github.com/TentativeConvert/LaTeX-Note-Importer-for-Anki))
--- an Anki add-on that extracts and imports Anki notes from a LaTeX file.


## Links to articles on using Anki

- [Everything I Know: Strategies, Tips, and Tricks for Anki](https://senrigan.io/blog/everything-i-know-strategies-tips-and-tricks-for-spaced-repetition-anki/?utm_source=hackernewsletter&utm_medium=email&utm_term=fav)
- [Memorizing a programming language using spaced repetition software | Derek Sivers](https://sivers.org/srs)
- [LearnItFast](https://learnitfast.io/#/)
- [Augmenting Long-term Memory](http://augmentingcognition.com/ltm.html)
- [Using spaced repetition systems to see through a piece of mathematics](http://cognitivemedium.com/srs-mathematics)

