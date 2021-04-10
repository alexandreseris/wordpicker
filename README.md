# wordpicker

Command line utility to generate random word in given language. Also support word transformations  
*tested on python 3.6*

Based on [Words](https://github.com/lorenbrichter/Words) for the word lists

## Usage

```sh
wordpicker.py lang minLenWord numberOfWords joinCharacter [-h] [-s] [-u] [-t]
```

positional arguments:

- `lang`: the code for the choosen language (eg: en, fr, es, de, etc...), you can check the available languages [here](https://github.com/lorenbrichter/Words/tree/master/Words)
- `minLenWord`: the minimal length of words choosen
- `numberOfWords`: number of words choosen
- `joinCharacter`: character used to join words

optional arguments:

- `-h`, `--help`: show this help message and exit
- `-s`, `--shuffleTransformation`: enable Shuffle transformation
- `-u`, `--upperTransformation`: enable Upper transformation
- `-t`, `--transpositionTransformation`: enable Transposition transformation
