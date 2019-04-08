from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
import pandas as pd
from DevJobs.settings import STACK_JOBS_DATA

vectorizer = None
tags_corr = None
df_tags = None
PATH_DATA = STACK_JOBS_DATA # 'data/'

def _aplicar_tfidf(palavras = []):
    palavras = [_clean_tranform_str(p) for p in palavras]
    matrix_tfidf = vectorizer.transform(palavras)
    
    return pd.DataFrame(
        matrix_tfidf.todense(),
        columns=vectorizer.get_feature_names()
    )

def _tag_similar(df_tags, df_tfidf_tags, df_tfidf_analizar):
    df_tfidf = df_tfidf_tags.append(df_tfidf_analizar, ignore_index=True)
    sim_matriz = cosine_similarity(df_tfidf)
    
    sim_serie = pd.Series(sim_matriz[-1]).sort_values(ascending=False)

    if sim_serie.iloc[1] > 0.4:
        index_tag = df_tags.loc[sim_serie.index[1]].name
        return df_tags.columns[index_tag]
    else: return None


def _tags_correlacionadas(tag):
    return tags_corr[ tag ].sort_values(ascending=False)[:20]

def _clean_tranform_str(texto):
    processado = ' '.join([x for x in texto])
    processado += ' ' +  ' '.join([texto[i:i+2] for i, x in enumerate(texto[:-1])])
    return processado

def obter_tags_correlacionadas(descricao):
    tfidf_analizar = _aplicar_tfidf([descricao])
    tag_similar = _tag_similar(df_tags, tfidf_tags, tfidf_analizar)
    
    if not tag_similar: return []
    
    tags_correlacionadas = _tags_correlacionadas(tag_similar)
    return tags_correlacionadas.index.tolist()
    
    
def _inicializa():
    global tags_corr, tfidf_tags, df_tags, vectorizer

    df_tags = pd.read_csv(PATH_DATA + 'jobs_tags.csv')
    df_tags = df_tags.drop(['id'],axis=1)

    vectorizer = joblib.load(PATH_DATA + 'vectorizer_tags.dat')
    tags_corr = df_tags.fillna(0).corr()
    tfidf_tags = _aplicar_tfidf(df_tags.columns)
    
_inicializa()    