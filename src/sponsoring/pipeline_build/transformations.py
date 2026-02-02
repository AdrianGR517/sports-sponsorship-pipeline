import regex as re
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import normalize

acronyms_dict = {'&': 'and', '|': 'or', '/': 'and', 'IT': 'information technology', 'PR': 'public relations',
            'PPE': 'Personal protective equipment', 'HVAC': 'Heating ventilation and air conditioning'}
pattern_translate = re.compile(r"(?<!\w)[&|/](?!\w)|\b(PR|IT|HVAC|PPE)\b")   
pattern_split = r' (?=[A-Z][a-z])'

def translate_acronyms(col):
    output = (
    col
      .astype(str)
      .apply(lambda x: pattern_translate.sub(
        lambda m: acronyms_dict.get(m.group(0), m.group(0)),x))
    )
    return(output)

def split_text(col: pd.Series) -> pd.Series:
    output = (
        col
        .str.split(r' (?=[A-Z][a-z])')
    )
    return(output)

def get_embeddings(texts: list[str], model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    emb = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
    emb1 = normalize(emb)
    return emb1

def cluster_agglomerative(embeddings, n_clusters=30):
    clusterer = AgglomerativeClustering(
    n_clusters=n_clusters,
    metric="cosine",
    linkage="average"
    )
    labels = clusterer.fit_predict(embeddings)
    
    return(labels)

def name_clusters(df, embeddings, label_col="cluster", text_col="category_clean"):
    names = {}

    for c in sorted(df[label_col].unique()):
        idx = df.index[df[label_col] == c].to_list()
        X = embeddings[idx]
        centroid = X.mean(axis=0)

        sims = X @ centroid
        best = idx[int(np.argmax(sims))]

        names[c] = df.loc[best, text_col]

    df["cluster_name"] = df[label_col].map(names)
    return df

def industries_cluster_pipeline(col : pd.Series):
    col_translated = translate_acronyms(col)
    col_splitted = split_text(col_translated)
    col_flat = list(col_splitted.explode().dropna().unique())
    embeddings = get_embeddings(col_flat)
    labels = cluster_agglomerative(embeddings)
    df_ind = pd.DataFrame().from_dict({"category_clean":col_flat, "cluster":labels})
    df_clusters  = name_clusters(df_ind, embeddings)
    dict_cluster = dict(zip(df_clusters['category_clean'],df_clusters['cluster_name']))
    output = col_splitted.map(
        lambda lst: [
            dict_cluster.get(x, x) for x in lst
        ] if isinstance(lst, list) else lst
    )
    return(output.map(lambda x: set(x)))