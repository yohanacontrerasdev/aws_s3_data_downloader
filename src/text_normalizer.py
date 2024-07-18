import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    return text

def expand_contractions(text):
  
    contractions = {
        "can't": "cannot",
        "won't": "will not",
    }
    for contraction, expanded in contractions.items():
        text = re.sub(contraction, expanded, text)
    return text

def lemmatize_text(text):
    tokens = word_tokenize(text)
    lemmatized_text = ' '.join([lemmatizer.lemmatize(token) for token in tokens])
    return lemmatized_text

def remove_stopwords(text):
    tokens = word_tokenize(text)
    filtered_text = ' '.join([token for token in tokens if token not in stop_words])
    return filtered_text

def normalize_corpus(corpus, prefix='cleaned_text'):
    
    if isinstance(corpus, list):
        corpus = " ".join(corpus)

    corpus = clean_text(corpus)
    corpus = expand_contractions(corpus)
    corpus = lemmatize_text(corpus)
    corpus = remove_stopwords(corpus)

    output_file = f'{prefix}.txt'

    # Guardar el corpus en un archivo .txt
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(corpus)

    return corpus
