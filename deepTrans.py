# -*- coding: utf-8 -*-
"""Traductor de Idiomas"""

import speech_recognition as sr
import pandas as pd
from deep_translator import GoogleTranslator
import pyttsx3
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

#modelos Spacy de en_core_web_sm siempre no falta
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Modelo 'en_core_web_sm' no encontrado. Instalándolo ahora...")
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load('en_core_web_sm')

def get_lang_detector(nlp, name):
    return LanguageDetector()

try:
    Language.factory("language_detector", func=get_lang_detector)
except:
    pass
nlp.add_pipe('language_detector', last=True)

def Intersection(lst1, lst2):
    return set(lst1).intersection(lst2)

def cstr(s, color='black', size='50'):
    return s

def print_color(s):
    print(' '.join(ti for ti, _, _ in s))

r = sr.Recognizer()
r.energy_threshold = 300
translator = GoogleTranslator(source='auto', target='es')
lista_fr = stopwords.words('french')
lista_pt = stopwords.words('portuguese')
lista_es = stopwords.words('spanish')
lista_en = stopwords.words('english')
engine = pyttsx3.init()
engine.setProperty('rate', 200)
engine.setProperty('volume', 1)
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-MX_SABINA_11.0')

def reconocer(sonido):
    lista = ['fr-FR', 'pt-BR', 'es-ES', 'en-US']
    fr, pt, es, en = 0, 0, 0, 0
    df = pd.DataFrame(columns=['query', 'idioma', 'valor', 'palabras', 'stopwords', 'idioma_final', 'match', 'nota'])

    for elemento in lista:
        try:
            query = r.recognize_google(sonido, language=elemento)
            print(f"Reconocido con {elemento}: '{query}'")
            valor = nlp(query)._.language.get('score')
            idioma = nlp(query)._.language.get('language')
            print(f"SpaCy detectó idioma: {idioma}, puntaje: {valor}")
            palabras = len(query.split())
            stopwords = 0
            if elemento == 'fr-FR':
                stopwords, fr, idioma_final = len(Intersection(query.split(), lista_fr)), (fr+1), 'Frances'
                idioma = 'fr'
            elif elemento == 'pt-BR':
                stopwords, pt, idioma_final = len(Intersection(query.split(), lista_pt)), (pt+1), 'Portugues'
                idioma = 'pt'
            elif elemento == 'es-ES':
                stopwords, es, idioma_final = len(Intersection(query.split(), lista_es)), (es+1), 'Español'
                idioma = 'es'
            elif elemento == 'en-US':
                stopwords, en, idioma_final = len(Intersection(query.split(), lista_en)), (en+1), 'Ingles'
                idioma = 'en'
            df.loc[len(df)] = [query, idioma, valor, palabras, stopwords, idioma_final, 0, 0.0]
        except Exception as e:
            print(f"Error con {elemento}: {e}")
            continue

    for index, row in df.iterrows():
        if row['idioma'] == 'fr':
            df.at[index, 'match'] = fr
        if row['idioma'] == 'pt':
            df.at[index, 'match'] = pt
        if row['idioma'] == 'es':
            df.at[index, 'match'] = es
        if row['idioma'] == 'en':
            df.at[index, 'match'] = en

    df['nota'] = (df['palabras'] + df['stopwords']) * df['valor'] * df['match']
    resultado = df[df['nota'] == df['nota'].max()]

    if len(resultado) > 0:
        print_color([(resultado['idioma_final'].values[0] + ' detectado', 'blue', '40')])
        return resultado['query'].values[0], resultado['idioma'].values[0]
    else:
        return 'Nada', None

def takecommand():
    try:
        with sr.Microphone(device_index=2) as source:
            print("Ajustando al ruido ambiental...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Escuchando...")
            audio = r.listen(source, timeout=6, phrase_time_limit=5)
    except ValueError as e:
        print(f"Error al inicializar el micrófono: {e}")
        return "None"
    except Exception as e:
        print(f"Error al capturar audio: {e}")
        return "None"

    try:
        mensaje, idioma_detectado = reconocer(audio)
        print_color((('La persona dijo: ', 'blue', '35'), (mensaje, 'black', '35')))
        if mensaje != 'Nada':
            dest = 'es' if idioma_detectado != 'es' else 'en'
            translator.target = dest
            text = translator.translate(mensaje)
            print_color((('La traducción es: ', 'blue', '35'), (text, 'black', '35')))
            print("\n")
            engine.say(text)
            engine.runAndWait()
    except Exception as e:
        print(f"Error al procesar el audio: {e}")
        return "None"

    return mensaje

while True:
    query = takecommand()