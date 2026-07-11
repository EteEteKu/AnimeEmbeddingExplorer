import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity

def genre_similarity(anime_id1: int, anime_id2: int, dataFrame: pd.DataFrame) -> float:
    genres1 = dataFrame.at[anime_id1, "Genres_set"]
    genres2 = dataFrame.at[anime_id2, "Genres_set"]
    union = genres1 | genres2
    if len(union) == 0:
        return 0.0 
    return len(genres1 & genres2) / len(union)
def description_similarity(anime_id1: int, anime_id2: int,dataFrame: pd.DataFrame) -> float:
    vec1 = dataFrame.at[anime_id1, "embedding"].reshape(1, -1)
    vec2 = dataFrame.at[anime_id2, "embedding"].reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]
def total_similarity(anime_id1: int, anime_id2: int,dataFrame: pd.DataFrame) -> float:
    w_desc:float = 0.7
    w_genre:float = 0.3
    genre_score = genre_similarity(anime_id1, anime_id2,dataFrame)
    desc_score = description_similarity(anime_id1, anime_id2,dataFrame)
    return w_genre * genre_score + w_desc * desc_score