
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd 
from searchSimAnime import search_anime
DATAFRAME = pd.read_pickle(r"Animedataset\anime_processed.pkl")



app = FastAPI()

class AnimeRequest(BaseModel):
    anime_id:int 
    limit:int = 10
    min_similarity:float = 0.4


@app.post("/anime/similar")
def get_anime_similarity(request:AnimeRequest):
    similar = search_anime(
        request.anime_id,
        10,
        DATAFRAME,
        0.4
    )
    return {

        "anime_id":request.anime_id,
        "similar": similar
    }
@app.get("/")
def read_root():
    return {"message":"Hello world"}

