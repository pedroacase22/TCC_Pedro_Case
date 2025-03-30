import os
import string
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Baixar recursos do NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Caminho da pasta dos arquivos
pasta = r"C:\Users\pedro\OneDrive\tcc_python\leis"

# Arquivos das leis
arquivos = {
    "Bahia": "lei_bahia.txt",
    "Ceará": "lei_ceara.txt",
    "Pernambuco": "lei_pernambuco.txt",
    "Rio Grande do Norte": "lei_rn.txt"
}

# Leitura dos textos
texts = {}
for estado, arquivo in arquivos.items():
    with open(os.path.join(pasta, arquivo), "r", encoding="utf-8") as f:
        texts[estado] = f.read()

# ------------------------------------------
# DICIONÁRIO DE TERMOS (com expressões compostas)
# ------------------------------------------
dicionario_bruto = """
    "qualificação", "formação", "treinamento", "capacitação", "recursos humanos", "aprendizado", "capital intelectual",
    "regionalização", "interiorização", "desconcentração", "desenvolvimento local", "desigualdades", "descentralização", "inclusão", "interior", "igualdade",
    "startup", "empreendedorismo", "empreendedorismo inovador", "spin-offs", "aceleradoras", "incubadoras", "hackathons", "empresas inovadoras", "empreendimentos inovadores", "empreendimentos",
    "setor produtivo", "indústria", "competitividade", "ICTI", "inovação aberta", "empresas", "mercado", "empresas de pequeno porte", "sistema produtivo local", "ambiente produtivo", "pequena empresa", "microempresas",
    "fundos", "financiamento", "crédito", "capital de risco", "fomento", "incentivo fiscal", "royalties", "capitais", "bônus tecnológico", "fundos de investimento", "participação societária", "subvenção", "incentivo",
    "ICT", "ICTs", "universidade", "instituto", "NIT", "instituições científicas", "centro de pesquisa", "ensino superior", "ensino", "extensão", "pesquisa científica", "pesquisa científica e tecnológica", "inventor independente",
    "laboratórios", "laboratoriais", "centros tecnológicos", "espaços de inovação", "infraestrutura científica", "infraestrutura", "centros", "ambientes", "espaços", "fundação", "fundações de apoio", "obras", "conselho", "ecossistema", "polos tecnológicos", "parques tecnológicos", "hubs", "redes", "ambientes de inovação", "agência de fomento", "promotores",
    "compras públicas", "administração pública", "contrato público", "servidor", "pesquisador público", "empregado público", "licitação", "autarquias",
    "transferência de tecnologia", "desenvolvimento de tecnologia", "experimentação", "P&D", "PD&I", "licenciamento", "convênio", "transferência tecnológica"

"""

# Transformar o dicionário em lista de termos compostos
# Remove duplicatas mantendo a ordem original
termos_compostos = list(dict.fromkeys(
    [t.strip().strip('"').lower() for linha in dicionario_bruto.strip().split('\n') for t in linha.split(',')]
))



# ------------------------------------------
# PRÉ-PROCESSAMENTO (sem remover espaços entre palavras!)
# ------------------------------------------
def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('portuguese')]
    return " ".join(tokens)

texts_cleaned = {estado: preprocess_text(texto) for estado, texto in texts.items()}

# ------------------------------------------
# TF-IDF com n-gramas (1 a 3) e vocabulário manual
# ------------------------------------------
vectorizer = TfidfVectorizer(ngram_range=(1, 3), vocabulary=termos_compostos)
tfidf_matrix = vectorizer.fit_transform(texts_cleaned.values())

# DataFrame TF-IDF
df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), index=texts_cleaned.keys(), columns=vectorizer.get_feature_names_out())
print("\nMatriz TF-IDF (primeiras 10 colunas):\n")
print(df_tfidf.iloc[:, :10])

# ------------------------------------------
# SIMILARIDADE DO COSSENO
# ------------------------------------------
cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
df_similarity = pd.DataFrame(cosine_sim_matrix, index=texts_cleaned.keys(), columns=texts_cleaned.keys())
print("\nMatriz de Similaridade do Cosseno:\n")
print(df_similarity)

