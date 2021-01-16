import requests
import pathlib
import os
import sqlite3
import secrets

transpositionDict = {
    "a": "4",
    "b": "8",
    "c": "(",
    "d": "|)",
    "e": "3",
    "f": "|=",
    "g": "6",
    "h": "#",
    "i": "!",
    "j": "_|",
    "k": "|<",
    "l": "|",
    "m": "|v|",
    "n": "|V",
    "o": "()",
    "p": "|*",
    "q": "(_,)",
    "r": "2",
    "s": "5",
    "t": "7",
    "u": "(_)",
    "v": "\\/",
    "w": "\\/\\/",
    "x": "><",
    "y": "7",
    "z": "2"
}


def shuffle(word):
    if len(word) <= 1:
        return word
    else:
        newWord = ""
        characterList = list(word)
        while len(characterList) > 0:
            randomChar = secrets.choice(characterList)
            newWord += randomChar
            characterList.remove(randomChar)
        return newWord


def wordTransformation(word, shuffleTransformation=True, upperTransformation=True, transpositionTransformation=True):
    def transposition(letter):
        try:
            return transpositionDict[letter]
        except KeyError:
            print("transposition for {} undefined, using raw letter instead".format(letter))
            return letter
    transformedWord = ""
    if shuffleTransformation and secrets.randbelow(2) == 1:
        word = shuffle(word)
    characterTransformationsOptions = [
        [upperTransformation, lambda letter: letter.upper()],
        [transpositionTransformation, lambda letter: transposition(letter)]
    ]
    characterTransformationsOptionsActive = [opt for opt in characterTransformationsOptions if opt[0] is True]
    if len(characterTransformationsOptionsActive) > 0:
        for letter in word:
            randomRoll = secrets.randbelow(len(characterTransformationsOptionsActive) + 1)
            if randomRoll == 0:
                transformedWord += letter
            else:
                transformedWord += characterTransformationsOptionsActive[randomRoll - 1][1](letter)
    else:
        return word
    return transformedWord


def wordpicker(lang, minLenWord, numberOfWords, joinCharacter, shuffleTransformation, upperTransformation, transpositionTransformation):
    appDir = os.path.join(str(pathlib.Path.home()), ".wordpicker")
    if not os.path.isdir(appDir):
        print("creating wordpicker directory to store word list")
        os.mkdir(appDir)
    langFile = os.path.join(appDir, lang)

    def listFromGithub(lang):
        def getWordList():
            url = "https://raw.githubusercontent.com/lorenbrichter/Words/master/Words/{}.txt".format(lang)
            print("downloading list from {}".format(url))
            req = requests.get(url)
            return req.content.decode("utf-8").split("\n")
        return getWordList

    langFileGetter = {
        "en": listFromGithub("en"),
        "de": listFromGithub("de"),
        "fr": listFromGithub("fr"),
        "es": listFromGithub("es"),
    }

    dbFileExists = os.path.isfile(langFile)
    if lang not in langFileGetter.keys():
        print("sorry, lang {} is not available, languages availables are: {}".format(lang, ",".join(langFileGetter.keys())))

    conn = sqlite3.connect(langFile)
    cur = conn.cursor()

    if not dbFileExists:
        print("creating database in {}".format(langFile))
        wordList = langFileGetter[lang]()
        cur.execute("PRAGMA encoding = 'UTF-8';")
        cur.execute("create table words (word text);")
        cur.execute("create unique index words_idx on words(word);")
        conn.commit()
        for word in wordList:
            if word != "":
                try:
                    cur.execute("insert into words values (?);", (word.lower(),))
                except sqlite3.IntegrityError:
                    print("{} alredy in db".format(word))
        conn.commit()

    wordList = cur.execute("select word from words where length(word) >= ?", (minLenWord,)).fetchall()

    cur.close()
    conn.close()

    choosenWords = []
    currentNbrWords = 0
    while currentNbrWords < numberOfWords:
        randomWord = secrets.choice(wordList)
        choosenWords.append(randomWord[0])
        wordList.remove(randomWord)
        currentNbrWords += 1
    if True in (shuffleTransformation, upperTransformation, transpositionTransformation):
        return joinCharacter.join([wordTransformation(word, shuffleTransformation=shuffleTransformation, upperTransformation=upperTransformation, transpositionTransformation=transpositionTransformation)
                        for word in choosenWords]
                                  )
    else:
        return joinCharacter.join(choosenWords)


if __name__ == "__main__":
    import sys
    import argparse

    argParser = argparse.ArgumentParser(description="command line utility to generate random word in given language. Also support word transformations")
    argParser.add_argument("lang", nargs=1, type=str, help="the choosen language")
    argParser.add_argument("minLenWord", nargs=1, type=int, help="the minimal length of words choosen")
    argParser.add_argument("numberOfWords", nargs=1, type=int, help="number of words choosen")
    argParser.add_argument("joinCharacter", nargs=1, type=str, help="character used to join words")
    argParser.add_argument("-s", "--shuffleTransformation", action="store_true", help="enable Shuffle transformation")
    argParser.add_argument("-u", "--upperTransformation", action="store_true", help="enable Upper transformation")
    argParser.add_argument("-t", "--transpositionTransformation", action="store_true", help="enable Transposition transformation")

    argsParsed = argParser.parse_args(sys.argv[1:])
    lang = argsParsed.lang[0]
    minLenWord = argsParsed.minLenWord[0]
    numberOfWords = argsParsed.numberOfWords[0]
    joinCharacter = argsParsed.joinCharacter[0]
    shuffleTransformation = argsParsed.shuffleTransformation
    upperTransformation = argsParsed.upperTransformation
    transpositionTransformation = argsParsed.transpositionTransformation

    print(wordpicker(lang, minLenWord, numberOfWords, joinCharacter, shuffleTransformation, upperTransformation, transpositionTransformation))
