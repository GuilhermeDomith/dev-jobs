from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from string import punctuation, digits
import nltk, pandas as pd, re
from DevJobs.settings import STACK_JOBS_DATA, UDEMY_DATA

vectorizer_curso = None
stopwords = None
tags = None
#stemmer = None
df_cursos = None
df_cursos_tfidf = None
vectorizer_tags = None
df_tfidf_tags = None

def _processar_texto(texto):
    
    texto = ' '.join([w for w in nltk.word_tokenize(texto) 
                          if (w not in punctuation and w not in stopwords) 
                            and not (re.match('.*[\d_].*', w) and w not in tags)
                     ])
    return texto

def _aplicar_tfidf(textos, vectorizer):
    matrix_tfidf = vectorizer.transform(textos)
    return pd.DataFrame(
        matrix_tfidf.todense(),
        columns=vectorizer.get_feature_names()
    )
    

def descobrir_tags_do_curso(desc_curso, corte_sim=0.20, max_tags=8):
    df_tfidf_cursos = _aplicar_tfidf([desc_curso], vectorizer_tags)
    df = df_tfidf_tags.append(df_tfidf_cursos, ignore_index=True)
    
    sim = cosine_similarity(df)
    sim = pd.Series(sim[-1][:-1])
    sim = sim[sim > corte_sim]
    
    index_tags_sim = sim.sort_values(ascending=False).index
    return pd.Series(tags)[index_tags_sim][:max_tags]  
    

def cursos_similares(search, max_cursos):
    search = _processar_texto(search)
    search_tfidf = _aplicar_tfidf([search], vectorizer_curso)
    
    df_tfidf = df_cursos_tfidf.append(search_tfidf, ignore_index=True)
    sim = cosine_similarity(df_tfidf)
    index_cursos = pd.Series(sim[-1]).sort_values(ascending=False).index
    
    return df_cursos.reindex(index_cursos[1:max_cursos+1]).to_dict(orient='records')
    
    

def _inicializar():
    global stopwords, df_cursos, df_cursos_tfidf, vectorizer_curso, tags, vectorizer_tags, df_tfidf_tags
    
    stopwords = nltk.corpus.stopwords.words('english')
    tags = pd.read_csv(STACK_JOBS_DATA + 'jobs_tags.csv').columns.tolist()
    
    df_cursos = pd.read_csv(UDEMY_DATA + 'cursos_udemy.csv')
    vectorizer_curso = joblib.load(UDEMY_DATA + 'vectorizer_cursos.dat')
    df_cursos_tfidf = pd.read_csv(UDEMY_DATA + 'cursos_tfidf.csv')

    vectorizer_tags = joblib.load(UDEMY_DATA + 'vectorizer_tags.dat')
    df_tfidf_tags = pd.read_csv(UDEMY_DATA + 'tags_tfidf.csv')
    
_inicializar()
