from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from nltk.util import ngrams
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob
from nltk.tokenize import word_tokenize
import seaborn as sns
import pandas as pd
import random
import nltk
import re

nltk.download('punkt')

def clean_text(text):
  text = re.sub(r'\s*\|\s*', ' ', text)
  text = re.sub(r'(?<!\w)-(?!\w)', ' ', text)
  text = re.sub(r'\s+', ' ', text)
  return text

def analyze_text(cleaned_text, stop_words='english', words_per_segment=50):
  cleaned_text = clean_text(cleaned_text)

  # Tokenizar el texto
  words = word_tokenize(cleaned_text)

  # Agrupar tokens en segmentos de longitud fija
  documents = [' '.join(words[i:i+words_per_segment]) for i in range(0, len(words), words_per_segment)]

  # Inicializar CountVectorizer
  cv = CountVectorizer(stop_words=stop_words)

  # Ajustar y transformar los documentos
  X = cv.fit_transform(documents)

  vocab = cv.get_feature_names_out()

  # Número de palabras en el vocabulario
  random_sample_size = 10
  vocab_sample = random.sample(list(vocab), min(random_sample_size, len(vocab)))

  # Número de palabras en el vocabulario
  num_words = len(vocab)

  return X, num_words, vocab_sample

def analyze_sentiment(text):
	cleaned_text = clean_text(text)

	analysis = TextBlob(cleaned_text)
	return analysis.sentiment

def generate_word_cloud(cleaned_text, title='Word Cloud'):
	"""
	Generates and displays a Word Cloud based on the provided text.

	Parameters:
	cleaned_text (str): The cleaned and normalized text from which to generate the Word Cloud.
	title (str): The title of the plot.
	"""
	# Generate Word Cloud
	wordcloud = WordCloud(width=800, height=400, background_color='white').generate(cleaned_text)

	# Display Word Cloud
	plt.figure(figsize=(10, 5))
	plt.imshow(wordcloud, interpolation='bilinear')
	plt.axis('off')
	plt.title(title)
	plt.show()

def plot_common_words(cleaned_text, num_words=20):
	"""
	This function takes a text, tokenizes it, counts the frequency of the words,
	and generates a bar plot with the most common words.

	Parameters:
	cleaned_text (str): The text to analyze.
	num_words (int): The number of most common words to display in the plot.

	Returns:
	None
	"""
	# Clean the text
	cleaned_text_no_special_chars = clean_text(cleaned_text)

	# Tokenize the text into words
	tokens = nltk.word_tokenize(cleaned_text_no_special_chars)

	# Count the frequency of the words
	word_freq = Counter(tokens)

	# Get the most common words
	common_words = word_freq.most_common(num_words)
	words, counts = zip(*common_words)

	# Create bar plot
	plt.figure(figsize=(10, 5))
	sns.barplot(x=list(counts), y=list(words))
	plt.title('Common Words Frequency')
	plt.xlabel('Frequency')
	plt.ylabel('Words')
	plt.show()

def generate_ngrams(words, n):
 """
 Genera n-grams a partir de una lista de palabras usando nltk.
 """
 return list(ngrams(words, n))

def get_ngrams(text, n):
 """
 Limpia el texto, genera n-grams y cuenta su frecuencia.
 """
 # Limpiar el texto
 cleaned_text = clean_text(text)
 # Dividir el texto en palabras
 words = cleaned_text.split()
 # Generar n-grams
 ngrams = generate_ngrams(words, n)
 # Contar la frecuencia de los n-grams
 ngram_freq = Counter(ngrams)
 # Convertir a DataFrame para facilitar el análisis
 ngram_df = pd.DataFrame(ngram_freq.items(), columns=['ngram', 'frequency']).sort_values(by='frequency', ascending=False)
 ngram_df['ngram'] = ngram_df['ngram'].apply(lambda x: ' '.join(x))  # Convertir tuplas a strings
 return ngram_df

def plot_ngrams(ngram_df, top_n=10):
 """
 Visualiza los n-grams más comunes en un gráfico de barras.
 """
 # Seleccionar los top_n n-grams más comunes
 top_ngrams = ngram_df.head(top_n)
 # Crear gráfico de barras
 plt.figure(figsize=(10, 4))
 plt.bar(top_ngrams['ngram'], top_ngrams['frequency'])
 plt.xticks(rotation=45)
 plt.title(f'Top {top_n} N-grams más Comunes')
 plt.xlabel('N-grams')
 plt.ylabel('Frecuencia')
 plt.show()

def display_ngrams_with_plot_side_by_side(text, n=2, top_n=10):
 """
 Muestra los n-grams más comunes en una tabla y un gráfico de barras, uno al lado del otro.
 """
 ngram_df = get_ngrams(text, n)
 top_ngrams = ngram_df.head(top_n)

 fig, ax = plt.subplots(1, 2, figsize=(10, 4))

 # Tabla de n-grams
 ax[0].axis('off')
 table = ax[0].table(cellText=top_ngrams.values, colLabels=top_ngrams.columns, cellLoc='center', loc='center')
 table.scale(1, 1.5)
 table.auto_set_font_size(False)
 table.set_fontsize(10)
 ax[0].set_title(f'Top {top_n} N-grams', fontsize=10)

 # Gráfico de barras
 ax[1].bar(top_ngrams['ngram'], top_ngrams['frequency'])
 ax[1].set_xticks(range(len(top_ngrams['ngram'])))
 ax[1].set_xticklabels(top_ngrams['ngram'], rotation=45, ha='right', fontsize=8)
 ax[1].set_title(f'Top {top_n} N-grams más Comunes', fontsize=10)
 ax[1].set_xlabel('N-grams', fontsize=10)
 ax[1].set_ylabel('Frecuencia', fontsize=10)

 plt.tight_layout()
 plt.show()
