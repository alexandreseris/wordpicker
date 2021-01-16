# wordpicker

command line utility to generate random word in given language. Also support word transformations
tested on python 3.6

based on [lorenbrichter/Words](https://github.com/lorenbrichter/Words) for the word list, give him a star for his work!

```
usage: wordpicker.py [-h] [-s] [-u] [-t]
                     lang minLenWord numberOfWords joinCharacter

positional arguments:
  lang                  the choosen language
  minLenWord            the minimal length of words choosen
  numberOfWords         number of words choosen
  joinCharacter         character used to join words

optional arguments:
  -h, --help            show this help message and exit
  -s, --shuffleTransformation
                        enable Shuffle transformation
  -u, --upperTransformation
                        enable Upper transformation
  -t, --transpositionTransformation
                        enable Transposition transformation
```
