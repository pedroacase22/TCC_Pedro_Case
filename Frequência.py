import os
import string
import nltk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Baixar recursos
nltk.download("punkt")
nltk.download("stopwords")
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Caminho dos textos
pasta = r"C:\Users\pedro\OneDrive\tcc_python\leis"
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

# Pré-processamento leve (sem stemming, mantendo compostos possíveis)
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

texts_cleaned = {estado: preprocess(texto) for estado, texto in texts.items()}

# Dicionário original por tópico
TOPICOS = {
    "PD&I": [
        "transferência de tecnologia", "desenvolvimento de tecnologia", "experimentação", "p&d", "pd&i",
        "licenciamento", "convênio", "transferência tecnológica"
    ],
    "Capacitação e Formação": [
        "qualificação", "formação", "treinamento", "capacitação", "recursos humanos", "aprendizado", "capital intelectual"
    ],
    "Infraestrutura e Ambientes de Inovação": [
        "laboratórios", "laboratoriais", "centros tecnológicos", "espaços de inovação", "infraestrutura científica",
        "infraestrutura", "centros", "ambientes", "espaços", "fundação", "fundações de apoio", "obras", "conselho",
        "ecossistema", "polos tecnológicos", "parques tecnológicos", "hubs", "redes", "ambientes de inovação",
        "agência de fomento", "promotores"
    ],
    "ICTs e Universidades": [
        "ict", "icts", "universidade", "instituto", "nit", "instituições científicas", "centro de pesquisa",
        "ensino superior", "ensino", "extensão", "pesquisa científica", "pesquisa científica e tecnológica",
        "inventor independente"
    ],
    "Empreendedorismo e Startups": [
        "startup", "empreendedorismo", "empreendedorismo inovador", "spin-offs", "aceleradoras", "incubadoras",
        "hackathons", "empresas inovadoras", "empreendimentos inovadores", "empreendimentos", "microempresas"
    ],
    "Empresas e Mercado": [
        "setor produtivo", "indústria", "competitividade", "inovação aberta", "empresas", "mercado",
        "empresas de pequeno porte", "sistema produtivo local", "ambiente produtivo", "pequena empresa", "microempresas"
    ],
    "Financiamento e Fundos": [
        "fundos", "financiamento", "crédito", "capital de risco", "fomento", "incentivo fiscal", "royalties",
        "capitais", "bônus tecnológico", "fundos de investimento", "participação societária", "subvenção", "incentivo"
    ],
    "Descentralização e Interiorização": [
        "regionalização", "interiorização", "desconcentração", "desenvolvimento local", "desigualdades",
        "descentralização", "inclusão", "interior", "igualdade"
    ],
    "Inovação no Setor Público": [
        "compras públicas", "administração pública", "contrato público", "servidor", "pesquisador público",
        "empregado público", "licitação", "autarquias"
    ]
}

# Criar vocabulário único a partir de todos os tópicos
vocabulario = list({termo.lower().strip() for termos in TOPICOS.values() for termo in termos})

# Vetorização TF-IDF com n-gramas
vectorizer = TfidfVectorizer(ngram_range=(1, 3), vocabulary=vocabulario)
tfidf_matrix = vectorizer.fit_transform(texts_cleaned.values())

# DataFrame de termos
df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), index=texts_cleaned.keys(), columns=vectorizer.get_feature_names_out())

# Agrupar os termos por tópico e somar os valores
resultados_agrupados = {}
for topico, termos in TOPICOS.items():
    termos_validos = [t for t in termos if t in df_tfidf.columns]
    resultados_agrupados[topico] = df_tfidf[termos_validos].sum(axis=1)

df_topicos_sem_stem = pd.DataFrame(resultados_agrupados)

# Normalizar por linha
df_topicos_sem_stem = df_topicos_sem_stem.div(df_topicos_sem_stem.sum(axis=1), axis=0)

# Exibir a matriz final completa no terminal
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

print("\nMatriz de Frequência dos Tópicos por Estado (normalizada):\n")
print(df_topicos_sem_stem)
