from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from nltk.util import ngrams
import seaborn as sns
import pandas as pd
import nltk
import re

nltk.download('punkt')

def clean_text(text):
	return re.sub(r"[^\w\s]", "", text)

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

def generate_ngrams_df(text, n):
	tokens = nltk.word_tokenize(text)
	# Generar n-grams
	n_grams = list(ngrams(tokens, n))   
	# Crear un DataFrame
	n_grams_df = pd.DataFrame(n_grams, columns=[f'word_{i+1}' for i in range(n)])
	
	return n_grams_df

def combine_ngrams(text, max_n):
  all_ngrams = []
	
  text = clean_text(text)
	
  for n in range(1, max_n + 1):
    n_grams_df = generate_ngrams_df(text, n)
    n_grams_df['ngram_size'] = n 
    all_ngrams.append(n_grams_df)

  combined_df = pd.concat(all_ngrams, ignore_index=True)

  return combined_df


