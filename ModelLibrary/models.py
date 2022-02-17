import string

from langdetect import detect, LangDetectException
from nltk import word_tokenize, SnowballStemmer
from nltk.corpus import stopwords

RussianSnowball_ = SnowballStemmer(language="russian")
EnglishSnowball_ = SnowballStemmer(language="english")


def RussianTokinizer(sentence: str):
    sentence = sentence.strip().lower()

    try:
        if detect(sentence) == "ru":
            sentence.replace("e", "е").replace("a", "а").replace("c", "с").replace("p", "р").replace("o", "о").replace(
                "M", "м").replace("H", "н").replace("B", "в")
            sentence.replace("не ", "не").replace("no ", "no")
    except LangDetectException:
        pass
    sentence.replace("\t", " ")
    for i in string.punctuation:
        if i in sentence and i != " ":
            sentence = sentence.replace(i, '')
    tokens = word_tokenize(sentence, language="russian")
    tokens = [i for i in tokens if i not in stopwords.words("russian")]
    tokens = [RussianSnowball_.stem(i) for i in tokens]
    return " ".join(tokens)


def EnglishTokinizer(sentence: str):
    sentence = sentence.strip().lower()
    sentence.replace("\t", " ")
    for i in string.punctuation:
        if i in sentence and i != " ":
            sentence = sentence.replace(i, '')
    tokens = word_tokenize(sentence, language="english")
    tokens = [i for i in tokens if i not in stopwords.words("english")]
    tokens = [EnglishSnowball_.stem(i) for i in tokens]
    return " ".join(tokens)
