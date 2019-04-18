from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
import nltk, pandas as pd, re
from string import punctuation
from DevJobs.settings import STACK_JOBS_DATA

df_jobs = None
vectorizer = None
stopwords = None
tags = None
stemmer = None
jobs_tfidf = None

def _processar_texto(texto):
    texto = ' '.join([stemmer.stem(w) for w in nltk.word_tokenize(texto) 
                          if w not in punctuation and
                             w not in stopwords and
                            # Remove os números mas mantém as tags que os contém
                            not (re.match('.*[\d_].*', w) and w not in tags)
                     ])
    return texto


def _aplicar_tfidf(palavras = []):
    global vectorizer
        
    matrix_tfidf = vectorizer.transform(palavras)
    
    return pd.DataFrame(
        matrix_tfidf.todense(),
        columns=vectorizer.get_feature_names()
    )


def jobs_similares(search, max_jobs):
    search = _processar_texto(search)
    search_tfidf = _aplicar_tfidf([search])

    df_tfidf = jobs_tfidf.append(search_tfidf, ignore_index=True)
    sim = cosine_similarity(df_tfidf)
    index_jobs = pd.Series(sim[-1]).sort_values(ascending=False).index
    
    return df_jobs.reindex(index_jobs[1:max_jobs+1]).to_dict(orient='records')
    
    

def _inicializar():
    global stopwords, tags, stemmer, df_jobs, vectorizer, jobs_tfidf

    df_jobs = pd.read_csv(STACK_JOBS_DATA + 'Stack_Overflow_Jobs.csv')
    df_jobs.fillna("", inplace=True)
    df_jobs['posted'] = pd.to_datetime(df_jobs.posted)
    df_tags = pd.read_csv(STACK_JOBS_DATA + 'jobs_tags.csv')
    jobs_tfidf = pd.read_csv(STACK_JOBS_DATA + 'jobs_tfidf.csv')
    vectorizer = joblib.load(STACK_JOBS_DATA + 'vectorizer_jobs.dat')

    stopwords = '' #nltk.corpus.stopwords.words('english')
    tags = df_tags.columns.tolist()

    stemmer = nltk.stem.RSLPStemmer()
    

_inicializar()

