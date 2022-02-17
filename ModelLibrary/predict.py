# import pickle

from langdetect import detect

from models import EnglishTokinizer, RussianTokinizer

# with open("models/EnglishModel.bf", "rb") as EnglishModel, \
#         open("models/RussianModel.bf", "rb") as RussianModel:
#     models_ = [pickle.load(RussianModel), pickle.load(EnglishModel)]
#
# with open("models/RussianVectorizer.bf", "rb") as RussianVectorizer, \
#         open("models/EnglishVectorizer.bf", "rb") as EnglishVectorizer:
#     vectorizers_ = [pickle.load(RussianVectorizer), pickle.load(EnglishVectorizer)]


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
