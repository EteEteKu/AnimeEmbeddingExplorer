import pandas as pd 
from sklearn.metrics.pairwise import cosine_similarity
from similarity import *
from title_matching import *
#model = SentenceTransformer('all-MiniLM-L6-v2')
#def parse_genres(genre_string):
#    return set(g for g in genre_string.split(","))
#anime_pandas["Genres_set"] = anime_pandas["Genres"].apply(parse_genres) 
#embeddings_list = model.encode(anime_pandas["Synopsis"].fillna("").tolist())
#anime_pandas["embedding"] = list(embeddings_list)
#anime_pandas = anime_pandas.set_index('anime_id')
#anime_pandas.to_pickle("anime_processed.pkl")
anime_pandas = pd.read_pickle(r"Animedataset\anime_processed.pkl")

anime1 = 31240
#anime2 = 17265
all_anime_id = anime_pandas.index.tolist()

def search_anime(anime_target, dataframe, top):
    counter = top
    all_anime = []
    for anime_id_2 in all_anime_id:
        total_sim = total_similarity(anime_target, anime_id_2, dataframe)
        if total_sim > 0.5 and anime_target!=anime_id_2 and not is_related(anime_pandas.at[anime_target,"Name"], anime_pandas.at[anime_id_2,"Name"]):
            counter-=1
            all_anime.append(anime_id_2)
        if counter == 0: break
        
    return all_anime

recomend = search_anime(anime1,anime_pandas, 20)
if not recomend:
    print("Не нашлось похожего тайтла")
else: 

    for anime_id in recomend:
        genre_score = genre_similarity(anime1, anime_id,anime_pandas)
        desc_score = description_similarity(anime1, anime_id,anime_pandas)
        sim = total_similarity(anime1,anime_id,anime_pandas)
        name = anime_pandas.at[anime_id,"Name"]
        print(f"{name}    {genre_score}    {desc_score}   {sim}")