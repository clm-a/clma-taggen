import nltk
from nltk import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from gensim.parsing.preprocessing import remove_stopwords, strip_punctuation, strip_numeric
import re
from nltk.corpus import wordnet


try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    try:
        nltk.download("punkt")
    except FileExistsError:
        pass

# Télécharger les ressources NLTK si nécessaire
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet')
nltk.download('omw-1.4')


def get_wordnet_pos(treebank_tag):
    """
    Convertit les tags POS de Treebank en tags POS de WordNet.
    """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # Par défaut, on considère que c'est un nom

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

    # Lemmatisation avec les POS tags
    lemmatizer = WordNetLemmatizer()
    tokens_pos = pos_tag(tokens)
    lemmatized_tokens = []
    for token, pos in tokens_pos:
        wordnet_pos = get_wordnet_pos(pos)
        lemmatized_token = lemmatizer.lemmatize(token, pos=wordnet_pos)
        lemmatized_tokens.append(lemmatized_token)

    # Re-POS tagger les tokens lemmatisés
    lemmatized_tokens_pos = pos_tag(lemmatized_tokens)

    # Filtrage des noms uniquement
    tokens = [token for token, pos in lemmatized_tokens_pos if pos in ('NN', 'NNS', 'NNP', 'NNPS')]
    return tokens
