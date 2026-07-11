from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd 
from searchSimAnime import search_anime
from searchAnime import searchAnime
from fastapi.middleware.cors import CORSMiddleware

DATAFRAME = pd.read_pickle(r"Animedataset/anime_processed.pkl")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://animeembeddingexplorer.onrender.com"],  #
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnimeRequest(BaseModel):
    anime_id:int 
    limit:int = 10
    min_similarity:float = 0.4
@app.post("/anime/similar")
def get_anime_similarity(request:AnimeRequest):
    similar = search_anime(
        request.anime_id,
        request.limit,
        DATAFRAME,
        request.min_similarity
    )
    return {

        "anime_id":request.anime_id,
        "similar": similar
    }

@app.get("/anime/search")
def get_search_anime(anime_name:str,limit:int=10):
    all_found_anime = searchAnime(anime_name,DATAFRAME,limit)
    return {
        "search_name":anime_name,
        "found": all_found_anime
    }