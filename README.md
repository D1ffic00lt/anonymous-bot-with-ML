# anonymous-bot-with-ML
```Python
import pickle
from ModelLibrary.predict import GetToxicity

with open("ModelLibrary/models/EnglishModel.bf", "rb") as EnglishModel, \
        open("ModelLibrary/models/RussianModel.bf", "rb") as RussianModel:
    models_ = [pickle.load(RussianModel), pickle.load(EnglishModel)]

with open("ModelLibrary/models/RussianVectorizer.bf", "rb") as RussianVectorizer, \
        open("ModelLibrary/models/EnglishVectorizer.bf", "rb") as EnglishVectorizer:
    vectorizers_ = [pickle.load(RussianVectorizer), pickle.load(EnglishVectorizer)]

print(GetToxicity("ПРИВЕТ КАК ДЕЛА&", models=models_, vectorizers=vectorizers_))
```
