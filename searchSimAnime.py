import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from similarity import *
from title_matching import *
import heapq
#model = SentenceTransformer('all-MiniLM-L6-v2')
#def parse_genres(genre_string):
#    return set(g for g in genre_string.split(","))
#anime_pandas["Genres_set"] = anime_pandas["Genres"].apply(parse_genres) 
#embeddings_list = model.encode(anime_pandas["Synopsis"].fillna("").tolist())
#anime_pandas["embedding"] = list(embeddings_list)
#anime_pandas = anime_pandas.set_index('anime_id')
#anime_pandas.to_pickle("anime_processed.pkl")


def all_description_similarities(anime_target: int, dataframe: pd.DataFrame) -> pd.Series:
    target_vec = dataframe.at[anime_target, "embedding"].reshape(1, -1)
    all_vecs = np.vstack(dataframe["embedding"].values)  
    sims = cosine_similarity(target_vec, all_vecs)[0]    
    return pd.Series(sims, index=dataframe.index)
def build_anime_dict(anime_id:int, sim:float, dataframe:pd.DataFrame):
    return{
        "anime_id":anime_id,
        "total_sim":float(sim), 
        "name": dataframe.at[anime_id,"Name"] if dataframe.at[anime_id,"English name"] == "UNKNOWN" else dataframe.at[anime_id,"English name"],
        "image_url":dataframe.at[anime_id,"Image URL"],
        "genres":dataframe.at[anime_id,"Genres"],
        "episodes": dataframe.at[anime_id,"Episodes"],
        "score": dataframe.at[anime_id, "Score"]
    }
def search_anime(anime_target: int, limit: int, dataframe: pd.DataFrame, min_similarity: float = 0.4):
    desc_sims = all_description_similarities(anime_target, dataframe)  

    heap = []
    for anime_id_2 in dataframe.index:
        if anime_id_2 == anime_target:
            continue
        if is_related(dataframe.at[anime_target, "Name"], dataframe.at[anime_id_2, "Name"]):
            continue

        genre_score = genre_similarity(anime_target, anime_id_2, dataframe)
        desc_score = desc_sims[anime_id_2]  
        total_sim = 0.3 * genre_score + 0.7 * desc_score

        if total_sim > min_similarity:
            heapq.heappush(heap, (total_sim, anime_id_2))
            if len(heap) > limit:
                heapq.heappop(heap)

    top_n = sorted(heap, key=lambda x: x[0], reverse=True)
    return [build_anime_dict(anime_id, sim, dataframe) for sim, anime_id in top_n]


