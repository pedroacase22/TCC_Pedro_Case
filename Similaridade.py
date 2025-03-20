import os

# Definir a pasta onde os arquivos estão salvos
pasta = r"C:\Users\pedro\OneDrive\tcc_python\leis"  # 🔹 Ajustado para seu caminho correto

# Dicionário para armazenar os textos das leis
texts = {}

# Lista de arquivos das leis estaduais
arquivos = {
    "Bahia": "lei_bahia.txt",
    "Ceará": "lei_ceara.txt",
    "Pernambuco": "lei_pernambuco.txt",
    "Rio Grande do Norte": "lei_rn.txt"
}

# Ler cada arquivo e armazenar o conteúdo no dicionário
for estado, arquivo in arquivos.items():
    caminho_completo = os.path.join(pasta, arquivo)  # 🔹 Cria o caminho completo do arquivo
    with open(caminho_completo, "r", encoding="utf-8") as f:
        texts[estado] = f.read()  # 🔹 Lê todo o conteúdo do arquivo e armazena no dicionário

# Exibir os primeiros 500 caracteres de cada lei para conferir a leitura
for estado, texto in texts.items():
    print(f"\n{estado}:\n{texto[:500]}...\n")  # 🔹 Mostra um trecho inicial do texto
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Baixar os pacotes do NLTK (caso ainda não estejam baixados)
nltk.download('punkt')
nltk.download('stopwords')

# Função para limpar os textos
def preprocess_text(text):
    text = text.lower()  # 🔹 Converte para minúsculas
    text = text.translate(str.maketrans("", "", string.punctuation))  # 🔹 Remove pontuação
    tokens = word_tokenize(text)  # 🔹 Tokeniza (divide em palavras)
    tokens = [word for word in tokens if word not in stopwords.words('portuguese')]  # 🔹 Remove stopwords
    return " ".join(tokens)  # 🔹 Junta as palavras limpas em um novo texto
# Aplicar o pré-processamento a todos os textos das leis estaduais
texts_cleaned = {estado: preprocess_text(texto) for estado, texto in texts.items()}

# Exibir os primeiros 300 caracteres dos textos limpos
for estado, texto in texts_cleaned.items():
    print(f"\n{estado} (Texto Limpo):\n{texto[:300]}...\n")
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Vetorização TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts_cleaned.values())

# Criar um DataFrame para visualizar os vetores TF-IDF
df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), index=texts_cleaned.keys(), columns=vectorizer.get_feature_names_out())

# Exibir as 10 primeiras colunas dos vetores TF-IDF
print("\nMatriz TF-IDF (primeiras 10 colunas):\n")
print(df_tfidf.iloc[:, :10])
from sklearn.metrics.pairwise import cosine_similarity

# Calcular a similaridade do cosseno
cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Criar um DataFrame para visualizar os resultados
df_similarity = pd.DataFrame(cosine_sim_matrix, index=texts_cleaned.keys(), columns=texts_cleaned.keys())

# Exibir matriz de similaridade
print("\nMatriz de Similaridade do Cosseno:\n")
print(df_similarity)

