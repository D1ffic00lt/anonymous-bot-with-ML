# Modelo de aprendizaje automático para la determinación de toxicidad
[![Code Size](https://img.shields.io/github/languages/code-size/D1ffic00lt/anonymous-bot-with-ML/tree/model)](https://github.com/D1ffic00lt/anonymous-bot-with-ML/tree/model)

[English](README.md) | [Русский](READMEru.md) | [Español](READMEes.md)

Este modelo está diseñado para determinar el nivel de toxicidad de las oraciones en ruso e inglés.
## Descripción de archivos y carpetas
Nombre de archivo o carpeta | Contenido de un archivo o carpeta
----------------|----------------------
[EnglishToxicModel](EnglishToxicModel) | Carpeta con código para crear un modelo para aprender palabras en inglés
[EnglishToxicModel/EnglishModel.bf](EnglishToxicModel/EnglishModel.bf) | Modelo final para inglés
[EnglishToxicModel/EnglishVectorizer.bf](EnglishToxicModel/EnglishVectorizer.bf) | Vectorizador final para inglés
[EnglishToxicModel/EnglishToxicModel.ipynb](EnglishToxicModel/EnglishToxicModel.ipynb) | Modelo de cuaderno de entrenamiento
[EnglishToxicModel/labeledEN.csv](EnglishToxicModel/labeledEN.csv) | Datos para entrenamiento
[RussianToxicModel](RussianToxicModel) | Carpeta con código para crear un modelo para aprender palabras en ruso
[RussianToxicModel/RussianModel.bf](RussianToxicModel/RussianModel.bf) | Modelo final para ruso
[RussianToxicModel/RussianVectorizer.bf](RussianToxicModel/RussianVectorizer.bf) | Vectorizador final para ruso
[RussianToxicModel/RussianToxicModel.ipynb](RussianToxicModel/RussianToxicModel.ipynb) | Modelo de cuaderno de entrenamiento
[RussianToxicModel/labeledEN.csv](RussianToxicModel/labeledEN.csv) | Datos para entrenamiento
[ModelLibrary](ModelLibrary) | Carpeta con código de modelo listo
[ModelLibrary/models](ModelLibrary/models) | Carpeta con modelos y vectorizadores
[ModelLibrary/models/EnglishModel.bf](ModelLibrary/models/EnglishModel.bf) | Modelo para ingles
[ModelLibrary/models/RussianModel.bf](ModelLibrary/models/RussianModel.bf) | Modelo para ruso
[ModelLibrary/models/EnglishVectorizer.bf](ModelLibrary/models/EnglishVectorizer.bf) | Vectorizador para ingles
[ModelLibrary/models/RussianVectorizer.bf](ModelLibrary/models/RussianVectorizer.bf) | Vectorizador para el idioma ruso
[ModelLibrary/predict.py](ModelLibrary/predict.py) | Código predictor de toxicidad
[requirements.txt](requirements.txt) | Archivo de bibliotecas

# Un ejemplo de uso del programa.
```Python
import pickle                                                                        # Cargando biblioteca para leer modelos
from ModelLibrary.predict import GetToxicity                                         # Cargando el programa de entrenamiento

with open("ModelLibrary/models/EnglishModel.bf", "rb") as EnglishModel,              # Cargando modelos
        open("ModelLibrary/models/RussianModel.bf", "rb") as RussianModel:           # Cargando modelos
    models_ = [pickle.load(RussianModel), pickle.load(EnglishModel)]                 # Cargando modelos

with open("ModelLibrary/models/RussianVectorizer.bf", "rb") as RussianVectorizer,    # Cargando vectorizadores
        open("ModelLibrary/models/EnglishVectorizer.bf", "rb") as EnglishVectorizer: # Cargando vectorizadores
    vectorizers_ = [pickle.load(RussianVectorizer), pickle.load(EnglishVectorizer)]  # Cargando vectorizadores

print(GetToxicity("ПРИВЕТ КАК ДЕЛА&", models=models_, vectorizers=vectorizers_))     # Predicción de toxicidad
```
