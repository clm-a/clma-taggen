import pandas as pd
import numpy as np
import gensim
from gensim.parsing.preprocessing import remove_stopwords, strip_punctuation, strip_numeric
import joblib
import os

import tags_generator.shared
from tags_generator.shared.preprocessing import preprocess_text
from tags_generator.word2vec.shared import get_document_vector

def load_model(path = 'tags_generator/word2vec/dumps'):
  w2v_model = gensim.models.Word2Vec.load(os.path.join(path, 'w2v_model.model'))
  classifier = joblib.load(os.path.join(path, 'classifier.pkl'))
  mlb = joblib.load(os.path.join(path, 'mlb.pkl'))
  return w2v_model, classifier, mlb

def suggest_tags(question, w2v_model, classifier, mlb):
  tokens = preprocess_text(question)
  doc_vector = get_document_vector(tokens, w2v_model).reshape(1, -1)
  pred = classifier.predict(doc_vector)
  tags = mlb.inverse_transform(pred)
  return tags[0]  # Retourne les tags sous forme de liste

