import re
import string
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def extract_tables_and_text(text):
  lines = text.split('\n')
  segments = []
  current_segment = []
  in_table = False

  for line in lines:
    if re.match(r'^\|.*\|$', line) or (in_table and re.match(r'^\|[-]+.*\|$', line)):
      if not in_table and current_segment:
          segments.append(('text', '\n'.join(current_segment)))
          current_segment = []
      in_table = True
      current_segment.append(line)
    else:
      if in_table:
          if current_segment:
              segments.append(('table', '\n'.join(current_segment)))
              current_segment = []
          in_table = False
      current_segment.append(line)
  
  if current_segment:
    segments.append(('table', '\n'.join(current_segment)) if in_table else ('text', '\n'.join(current_segment)))
  
  return segments

def clean_text(text):
  text = text.lower()  
  text = re.sub(r'\[.*?\]', '', text)  
  text = re.sub(r'https?://\S+|www\.\S+', '', text)
  text = re.sub(r'<.*?>+', '', text)
  text = re.sub(r'[%s]' % re.escape(string.punctuation.replace('.', '').replace('-', '').replace('$', '').replace(',', '').replace('%', '')), ' ', text)
  text = re.sub(r'\n', ' ', text)
  text = re.sub(r'\s+-\s+', ' ', text)
  text = re.sub(r'[^\w\s.$,%-]', '', text)
  text = re.sub(r'\s+', ' ', text)
  text = text.strip()
  return text

def expand_contractions(text):
  contractions = {
    "can't": "cannot",
    "won't": "will not",
  }
  for contraction, expanded in contractions.items():
    text = re.sub(r'\b{}\b'.format(contraction), expanded, text)
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

def clean_table_text(table_text):
  lines = table_text.split('\n')
  cleaned_lines = []

  for line in lines:
    if line.startswith('|') and line.endswith('|'):
      cells = line.split('|')
      cleaned_cells = [normalize_text(cell) for cell in cells]
      cleaned_line = '|'.join(cleaned_cells)
      cleaned_lines.append(cleaned_line)
    else:
      cleaned_lines.append(line)

  return '\n'.join(cleaned_lines)

def normalize_corpus(dataframes):
  normalized_dataframes = []

  for text in dataframes:
    segments = extract_tables_and_text(text)
    normalized_segments = []

    for segment_type, segment_text in segments:
      if segment_type == 'text':
          normalized_segments.append(normalize_text(segment_text))
      else:
          normalized_segments.append(clean_table_text(segment_text))
    
    combined_text = '\n\n'.join(normalized_segments)
    normalized_dataframes.append(combined_text)

  return pd.DataFrame(normalized_dataframes, columns=["Normalized Text"])
