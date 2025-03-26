install.packages("quanteda")
install.packages("quanteda.textstats")
install.packages("readtext")

library(quanteda)
library(quanteda.textstats)
library(readtext)

textos <- readtext("C:/Users/pedro/OneDrive/tcc_python/leis/*.txt", encoding = "UTF-8")
corp <- corpus(textos)

toks <- tokens(corp, remove_punct = TRUE)

meu_dicionario <- c(
  "P&D", "capacitação", "infraestrutura", "ambientes", 
  "ICTs", "universidades", "startups", "empreendedorismo", 
  "empresas", "financiamento", "descentralização", "setor público"
)

toks <- tokens_tolower(toks)
meu_dicionario <- tolower(meu_dicionario)

toks_inside <- tokens_keep(toks, pattern = meu_dicionario, window = 10)
toks_inside <- tokens_remove(toks_inside, pattern = meu_dicionario)

toks_outside <- tokens_remove(toks, pattern = meu_dicionario, window = 10)

dfmat_inside <- dfm(toks_inside)
dfmat_outside <- dfm(toks_outside)

tstat_key <- textstat_keyness(
  rbind(dfmat_inside, dfmat_outside),
  target = seq_len(ndoc(dfmat_inside))
)

head(tstat_key, 50)
