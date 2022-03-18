# Модель машинного обучения для определения токсичности
[![Code Size](https://img.shields.io/github/languages/code-size/D1ffic00lt/anonymous-bot-with-ML/tree/model)](https://github.com/D1ffic00lt/anonymous-bot-with-ML/tree/model)
 
[English](README.md) | [Русский](READMEru.md) | [Español](READMEes.md)
 
Данная модель предназначена для определения уровня токсичности предложений на русском и английском языках.
## Описание файлов и папок
Имя файла или папки  | Содержимое файла или папки
----------------|----------------------
[EnglishToxicModel](EnglishToxicModel) | Папка с кодом для создания модели для английских слов
[EnglishToxicModel/EnglishModel.bf](EnglishToxicModel/EnglishModel.bf) | Окончательная модель для английского языка
[EnglishToxicModel/EnglishVectorizer.bf](EnglishToxicModel/EnglishVectorizer.bf) | Окончательный векторизатор для английского языка
[EnglishToxicModel/EnglishToxicModel.ipynb](EnglishToxicModel/EnglishToxicModel.ipynb) | Блокнот для обучения модели
[EnglishToxicModel/labeledEN.csv](EnglishToxicModel/labeledEN.csv) | Данные для обучения
[RussianToxicModel](RussianToxicModel) | Папка с кодом для создания модели для изучения русских слов
[RussianToxicModel/RussianModel.bf](RussianToxicModel/RussianModel.bf) | Окончательная модель для русского языка
[RussianToxicModel/RussianVectorizer.bf](RussianToxicModel/RussianVectorizer.bf) | Окончательный векторизатор для русского языка
[RussianToxicModel/RussianToxicModel.ipynb](RussianToxicModel/RussianToxicModel.ipynb) | Блокнот для обучения модели
[RussianToxicModel/labeledEN.csv](RussianToxicModel/labeledEN.csv) | Данные для обучения
[ModelLibrary](ModelLibrary) | Папка с готовым кодом модели
[ModelLibrary/models](ModelLibrary/models) | Папка с моделями и векторизаторами
[ModelLibrary/models/EnglishModel.bf](ModelLibrary/models/EnglishModel.bf) | Английская модель
[ModelLibrary/models/RussianModel.bf](ModelLibrary/models/RussianModel.bf) | Русская модель
[ModelLibrary/models/EnglishVectorizer.bf](ModelLibrary/models/EnglishVectorizer.bf) | Английский векторизатор
[ModelLibrary/models/RussianVectorizer.bf](ModelLibrary/models/RussianVectorizer.bf) | Русский векторизатор
[ModelLibrary/predict.py](ModelLibrary/predict.py) | Код предиктора токсичности
[requirements.txt](requirements.txt) | Файл библиотеки

# Пример использования программы
```Python
import pickle                                                                        # Загрузка библиотеки для чтения моделей
from ModelLibrary.predict import GetToxicity                                         # Загрузка тренировочной программы

with open("ModelLibrary/models/EnglishModel.bf", "rb") as EnglishModel,              # Загрузка моделей
        open("ModelLibrary/models/RussianModel.bf", "rb") as RussianModel:           # Загрузка моделей
    models_ = [pickle.load(RussianModel), pickle.load(EnglishModel)]                 # Загрузка моделей

with open("ModelLibrary/models/RussianVectorizer.bf", "rb") as RussianVectorizer,    # Загрузка векторизаторов
        open("ModelLibrary/models/EnglishVectorizer.bf", "rb") as EnglishVectorizer: # Загрузка векторизаторов
    vectorizers_ = [pickle.load(RussianVectorizer), pickle.load(EnglishVectorizer)]  # Загрузка векторизаторов

print(GetToxicity("ПРИВЕТ КАК ДЕЛА&", models=models_, vectorizers=vectorizers_))     # Прогноз токсичности
```
