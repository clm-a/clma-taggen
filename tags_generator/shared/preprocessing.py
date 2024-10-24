import nltk
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from gensim.parsing.preprocessing import remove_stopwords, strip_punctuation, strip_numeric
import re

# Télécharger les ressources NLTK si nécessaire
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)

def preprocess_text(text):
    # Conversion en minuscules
    text = text.lower()
    # Suppression de la ponctuation et des caractères numériques
    text = strip_punctuation(text)
    text = strip_numeric(text)

    text = re.sub(r'c#', 'csharp', text)
    text = re.sub(r'c\+\+', 'cplusplus', text)
    text = re.sub(r'\.net', 'dotnet', text)
    # Suppression des stop words
    text = remove_stopwords(text)
    # Tokenisation
    tokens = word_tokenize(text)
    # Lemmatisation
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens
