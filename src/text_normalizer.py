import re
import string
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from src.contractions import CONTRACTION_MAP

import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def clean_text(text):
  text = text.lower()
  text = re.sub(r'https?://\S+|www\.\S+', '', text)
  text = re.sub(r'\s+', ' ', text)
  text = text.replace('®', '')
  text = text.strip()
  return text

def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
  contractions_pattern = re.compile(
      "({})".format("|".join(contraction_mapping.keys())),
      flags=re.IGNORECASE | re.DOTALL,
  )

  def expand_match(contraction):
      match = contraction.group(0)
      first_char = match[0]
      expanded_contraction = (
          contraction_mapping.get(match)
          if contraction_mapping.get(match)
          else contraction_mapping.get(match.lower())
      )
      expanded_contraction = first_char + expanded_contraction[1:]
      return expanded_contraction

  expanded_text = contractions_pattern.sub(expand_match, text)
  text = re.sub("'", "", expanded_text)

  return text

def lemmatize_text(text):
  tokens = word_tokenize(text)
  lemmatized_text = ' '.join([lemmatizer.lemmatize(token) for token in tokens])
  return lemmatized_text

def remove_stopwords(text):
  tokens = word_tokenize(text)
  filtered_text = ' '.join([token for token in tokens if token not in stop_words])
  return filtered_text

def normalize_text(text):
  text = clean_text(text)
  text = expand_contractions(text)
  text = lemmatize_text(text)
  text = remove_stopwords(text)
  return text

def normalize_corpus(dataframe):
  if 'text' not in dataframe.columns:
    raise ValueError("DataFrame must contain a 'text' column")
  
  normalized_texts = []
  
  for text in dataframe['text']:
    normalized_texts.append(normalize_text(text))
  
  return ' '.join(normalized_texts)
