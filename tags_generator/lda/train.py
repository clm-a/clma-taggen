# Importer les bibliothèques nécessaires
import pandas as pd
import numpy as np
import gensim
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamulticore import LdaMulticore
from gensim.parsing.preprocessing import remove_stopwords, strip_punctuation, strip_numeric, preprocess_string
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
import nltk
import joblib

import tags_generator.shared
from tags_generator.shared.preprocessing import preprocess_text
# Charger les données depuis le CSV
data = pd.read_csv('data/StackOverflow_tokenized2.csv', sep=',')

# Appliquer le prétraitement aux documents
documents = data['Body'].astype(str).apply(preprocess_text)

# Créer le dictionnaire et le corpus pour Gensim
id2word = Dictionary(documents)
corpus = [id2word.doc2bow(text) for text in documents]

# Entraîner le modèle LDA
num_topics = 10  # Vous pouvez ajuster ce nombre selon vos besoins
lda_model = LdaMulticore(corpus=corpus,
                         id2word=id2word,
                         num_topics=num_topics,
                         random_state=42,
                         chunksize=100,
                         passes=10,
                         workers=4)

# Obtenir les mots-clés pour chaque topic
topn = 10  # Nombre de mots-clés par topic
topic_keywords = {}
for topic_id in range(lda_model.num_topics):
    words = lda_model.show_topic(topic_id, topn=topn)
    topic_keywords[topic_id] = [word for word, prob in words]

lda_model.save('tags_generator/lda/dumps/lda_model.gensim')
id2word.save('tags_generator/lda/dumps/id2word.dict')
joblib.dump(topic_keywords, 'tags_generator/lda/dumps/topic_keywords.pkl')
