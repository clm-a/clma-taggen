import pandas as pd
import numpy as np
import os
import joblib
import sys
import gensim
from sklearn.preprocessing import MultiLabelBinarizer
from skmultilearn.model_selection import iterative_train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report

from tags_generator.shared.preprocessing import preprocess_text

# Fonction pour obtenir le vecteur moyen des mots d'une question
def get_document_vector(tokens, model):
    valid_tokens = [token for token in tokens if token in model.wv.key_to_index]
    if not valid_tokens:
        return np.zeros(model.vector_size)
    return np.mean(model.wv[valid_tokens], axis=0)

def train(input_file='data/monthly_best_1000_cleaned.csv', dump_path='tags_generator/word2vec/dumps'):
    # Charger les données
    data = pd.read_csv(input_file, sep=';')

    # Supposons que les tags sont dans une colonne 'Tags' sous forme de chaîne de caractères séparés par des virgules
    data['Tags'] = data['Tags'].astype(str).apply(lambda x: x.split(','))
    data['Body'] = data['Body'].astype(str).apply(lambda x: x.split(','))

    tokens_list = data['Body'].tolist()
    w2v_model = gensim.models.Word2Vec(sentences=tokens_list, vector_size=100, window=5, min_count=1, workers=4)

    data['Doc_Vector'] = data['Body'].apply(lambda tokens: get_document_vector(tokens, w2v_model))

    # Binariser les tags pour la classification multi-label
    mlb = MultiLabelBinarizer()
    y = mlb.fit_transform(data['Tags'])

    # Préparer les caractéristiques (X) et les labels (y)
    X = np.vstack(data['Doc_Vector'].values)

    X_np = X
    y_np = y

    # Diviser les données de manière stratifiée
    X_train, y_train, X_test, y_test = iterative_train_test_split(X_np, y_np, test_size=0.2)

    # Entraîner un modèle de régression logistique pour la classification multi-label
    classifier = OneVsRestClassifier(LogisticRegression(max_iter=1000))
    classifier.fit(X_train, y_train)

    # Prédire les tags sur l'ensemble de test
    y_pred = classifier.predict(X_test)

    # Générer un rapport de classification
    report = classification_report(y_test, y_pred, target_names=mlb.classes_)
    print(report)

    # Sauvegarder le modèle Word2Vec
    w2v_model.save(os.path.join(dump_path, 'w2v_model.model'))

    # Sauvegarder le classifieur
    joblib.dump(classifier, os.path.join(dump_path,'classifier.pkl'))

    # Sauvegarder le MultiLabelBinarizer
    joblib.dump(mlb, os.path.join(dump_path,'mlb.pkl'))

if __name__ == '__main__':
    if len(sys.argv) > 2:
        # Si des arguments supplémentaires sont fournis, on les passe à la fonction
        globals()[sys.argv[1]](*sys.argv[2:])
    elif len(sys.argv) > 1:
        # Si seule la fonction est fournie, on l'appelle sans arguments
        globals()[sys.argv[1]]()
    else:
        print("Veuillez fournir le nom de la fonction à exécuter.")
