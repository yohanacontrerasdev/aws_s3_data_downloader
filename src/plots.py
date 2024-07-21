from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generar_word_cloud(cleaned_text, title='Word Cloud'):
    """
    Genera y muestra un Word Cloud basado en el texto proporcionado.

    Parameters:
    cleaned_text (str): El texto limpio y normalizado del cual generar el Word Cloud.
    title (str): El título del gráfico.

    """
    # Generar Word Cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(cleaned_text)

    # Mostrar Word Cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.show()
