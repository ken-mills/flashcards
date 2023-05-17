# flashcards

flashcards.py is a windows command line script that displays words and translations imported from csv file. I wanted to practice French so I found the top 1000 French word list and scraped it from the internet. The list is ordered by most frequently used to least frequently used according to the source.

The script loops through the list of words and asks user to translate eash word. If correct, the word is moved to the next higher box of 3 virtual card boxes.

The user should study box 1 every day, study box 2 every 2 days, study box 3 every 5 days. This script is based on the [Leitner System](https://en.wikipedia.org/wiki/Leitner_system).

##Features
* Supports multiple groups of boxes for different types of lessons (numbers, frequency)
* Supports review mode to simply list the first 20 words in the box.

## Running script
`py flashcards.py T` - Run in Test mode to delete all boxes.

`py flashcards.py P` - Regular run mode

`py flashcards.py R` - Review mode displays the next 20 words from box 1

When running in T mode or running for the first time, the user is asked if they want to flip the translations in order to study the reverse.

When finished studying, hit Ctrl+C to interrupt script.




## script notes
When using windows 10 command line, python must run in utf-8 mode using one of two approaches
* You can use the Python UTF-8 Mode to change the default text encoding to UTF-8.
* You can enable the Python UTF-8 Mode via the -X utf8 command line option, #   or the PYTHONUTF8=1 environment variable.

Vitual card boxes are stored as json files and processed as lists in python

## Todo
* Some words are repeated, need to filter. Low priority because the extra practice is good.


