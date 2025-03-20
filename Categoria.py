from tcc import texts_cleaned  # Importa os textos já limpos

# Verificar se os textos foram importados corretamente
print(texts_cleaned.keys())  # Deve exibir os nomes dos estados: BA, CE, PE, RN
# Criar uma lista de tokens para cada texto
texts_tokens = {estado: text.split() for estado, text in texts_cleaned.items()}

# Conferir os primeiros tokens (opcional)
print(texts_tokens["Bahia"][:20])  # Exibe as 20 primeiras palavras do texto da Bahia
# Definir os tópicos e palavras-chave
TOPICOS = {
    "PD&I (Pesquisa, Desenvolvimento e Inovação)": ["inovação", "pesquisa", "desenvolvimento", "tecnologia", "experimentação", "P&D", "PD&I"],
    "Capacitação e Formação": ["qualificação", "formação", "treinamento", "ensino", "capacitação", "recursos humanos", "aprendizado"],
    "Infraestrutura de Inovação": ["laboratórios", "centros tecnológicos", "espaços de inovação", "infraestrutura científica", "ambientes colaborativos"],
    "ICTs e Universidades": ["ICT", "universidade", "instituto", "NIT", "instituições científicas", "centros de pesquisa", "ciência e tecnologia"],
    "Empreendedorismo e Startups": ["startups", "empreendedorismo inovador", "pequena empresa", "spin-offs", "aceleradoras"],
    "Empresas e Mercado": ["setor produtivo", "indústria", "empresas inovadoras", "competitividade", "transferência tecnológica", "inovação aberta"],
    "Ambientes de Inovação e Incubadoras": ["ecossistema de inovação", "polos tecnológicos", "parques tecnológicos", "incubadoras", "hubs", "hackathons"],
    "Financiamento e Fundos": ["fundos", "financiamento", "crédito", "capital de risco", "fomento", "incentivo fiscal", "royalties"],
    "Descentralização e Interiorização": ["regionalização", "interiorização", "desconcentração", "desenvolvimento local"],
    "Inovação no Setor Público": ["compras públicas", "administração pública", "investimento público", "contrato público", "política estatal", "inovação governamental"]
}
print(TOPICOS)
import pandas as pd
import pandas as pd
from collections import Counter

# Definir os tópicos e palavras-chave
TOPICOS = {
   
    "PD&I (Pesquisa, Desenvolvimento e Inovação)": [
        "transferência de tecnologia", "desenvolvimento de tecnologia", "experimentação",
        "p&d", "pd&i", "licenciamento", "convênio"
    ],
    "Capacitação e Formação": [
        "qualificação", "formação", "treinamento", "capacitação",
        "recursos humanos", "aprendizado", "capital intelectual"
    ],
    "Infraestrutura e Ambientes de Inovação": [
        "laboratórios", "laboratoriais", "centros tecnológicos", "espaços de inovação",
        "infraestrutura científica", "infraestrutura", "centros", "ambientes", "espaços",
        "fundação", "fundações de apoio", "obras", "conselho", "ecossistema de inovação",
        "polos tecnológicos", "parques tecnológicos", "hubs", "redes", "ambientes de inovação",
        "agência de fomento"
    ],
    "ICTs e Universidades": [
        "ICT", "ICTs", "universidade", "instituto", "NIT", "instituições científicas",
        "centro de pesquisa", "ensino superior", "ensino", "extensão",
        "pesquisa científica", "pesquisa científica e tecnológica", "inventor independente"
    ],
    "Empreendedorismo e Startups": [
        "startup", "empreendedorismo", "empreendedorismo inovador", "pequena empresa",
        "spin-offs", "aceleradoras", "incubadoras", "hackathons", "empresas inovadoras",
        "microempresas", "empreendimentos inovadores"
    ],
    "Empresas e Mercado": [
        "setor produtivo", "indústria", "competitividade", "transferência tecnológica",
        "inovação aberta", "empresas", "mercado", "microempresas", "empresas de pequeno porte",
        "sistema produtivo local", "ambiente produtivo"
    ],
    "Financiamento e Fundos": [
        "fundos", "financiamento", "crédito", "capital de risco", "fomento", "incentivo fiscal",
        "royalties", "capitais", "bônus tecnológico", "fundos de investimento", "participação societária"
    ],
    "Descentralização e Interiorização": [
        "regionalização", "interiorização", "desconcentração", "desenvolvimento local",
        "desigualdades", "descentralização", "inclusão", "interior"
    ],
    "Inovação no Setor Público": [
        "compras públicas", "administração pública", "contrato público",
        "servidor", "pesquisador público", "empregado público", "licitação"
    ]
}

# Função para contar a frequência dos tópicos nos textos
def contar_topicos(text):
    word_counts = Counter(text)  # Contar palavras no texto já tokenizado
    topicos_count = {
        topico: sum(word_counts.get(palavra, 0) for palavra in palavras)
        for topico, palavras in TOPICOS.items()
    }
    return topicos_count

# Aplicar a contagem para cada estado
resultados = {estado: contar_topicos(text) for estado, text in texts_tokens.items()}

# Criar um DataFrame para visualizar os resultados
df_resultados = pd.DataFrame(resultados).T

# Normalizar os valores para proporção
df_resultados = df_resultados.div(df_resultados.sum(axis=1), axis=0)

# Exibir a matriz gerada
print("\nMatriz de Frequência dos Tópicos por Estado:\n")
print(df_resultados)
# Ajustar pandas para exibir todas as colunas no terminal
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

# Exibir a matriz gerada
print("\nMatriz de Frequência dos Tópicos por Estado:\n")
print(df_resultados)
print(df_resultados.to_string())