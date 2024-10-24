
import gensim
from gensim.corpora.dictionary import Dictionary
import joblib

from tags_generator.shared.preprocessing import preprocess_text

def load_model():
    # Load the saved LDA model and dictionary
    lda_model = gensim.models.LdaMulticore.load('tags_generator/lda/dumps/lda_model.gensim')
    id2word = Dictionary.load('tags_generator/lda/dumps/id2word.dict')
    topic_keywords = joblib.load('tags_generator/lda/dumps/topic_keywords.pkl')
    return lda_model, id2word, topic_keywords


# Fonction pour suggérer des tags à partir d'une chaîne de caractères
def suggest_tags(user_input, lda_model, id2word, topic_keywords):
    # Prétraiter l'entrée utilisateur
    tokens = preprocess_text(user_input)
    # Transformer en Bag-of-Words
    bow_vector = id2word.doc2bow(tokens)
    # Obtenir la distribution des topics pour l'entrée
    topic_distribution = lda_model.get_document_topics(bow_vector, minimum_probability=0)
    # Identifier le topic dominant
    dominant_topic = max(topic_distribution, key=lambda x: x[1])[0]
    # Obtenir les tags suggérés à partir des mots-clés du topic dominant
    tags = topic_keywords[dominant_topic]
    # Optionnel : Intersecter avec les tokens de l'entrée utilisateur
    tags = list(set(tokens) & set(tags))
    # Si l'intersection est vide, utiliser les mots-clés du topic
    if not tags:
        tags = topic_keywords[dominant_topic]
    return tags
