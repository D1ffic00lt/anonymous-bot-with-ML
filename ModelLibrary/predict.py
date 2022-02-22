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


def GetToxicity(string_: str = None, models: list = None, vectorizers: list = None):
    if string_ is None or models is None or vectorizers is None:
        raise AttributeError("Argument not entered!")
    if detect(string_) in ["ru", "bg"]:
        toxic_propabality = models[0].predict_proba(vectorizers[0].transform(
            [RussianTokinizer(string_)]))[0, 1]
        return 1 if toxic_propabality >= 0.5 else 0, toxic_propabality
    else:
        toxic_propabality = models[1].predict_proba(vectorizers[1].transform(
            [EnglishTokinizer(string_)]))[0, 1]
        return 1 if toxic_propabality >= 0.5 else 0, toxic_propabality
