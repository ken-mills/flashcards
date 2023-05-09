# flashcards

flashcards.py is a windows command line script that displays words and translations imported from csv file.

The script loops through the list of words and asks user to translate eash word. If correct, the word is moved to the next higher box of 3 virtual card boxes.

The user should study box 1 every day, study box 2 every 2 days, study box 3 every 5 days. This script is based on the [Leitner System](https://en.wikipedia.org/wiki/Leitner_system).

when using windows 10 command line python must run in utf-8 mode using one of two approaches

## script notes
You can use the Python UTF-8 Mode to change the default text encoding to UTF-8. You can enable the Python UTF-8 Mode via the -X utf8 command line option, #   or the PYTHONUTF8=1 environment variable.

Boxes are stored as json files and processed as lists in python

