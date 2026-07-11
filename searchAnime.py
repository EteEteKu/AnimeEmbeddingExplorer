import pandas as pd 
import re
def build_anime_dict(anime_id:int, dataframe:pd.DataFrame):
    return{
        "anime_id":anime_id,
        "name": dataframe.at[anime_id,"Name"] if dataframe.at[anime_id,"English name"] == "UNKNOWN" else dataframe.at[anime_id,"English name"],
        "image_url":dataframe.at[anime_id,"Image URL"],
        "genres":dataframe.at[anime_id,"Genres"],
        "episodes": dataframe.at[anime_id,"Episodes"],
        "score": dataframe.at[anime_id, "Score"]
    }

def searchAnime(name:str, dataframe:pd.DataFrame, limit:int=10):
    name = (name.lower().strip())
    dataframe_sorted = dataframe.sort_values(by="Popularity",ascending=True)
    all_anime_id = dataframe_sorted.index.tolist()
    result = []
    for anime_id in all_anime_id:
        nameDT1 = str(dataframe_sorted.at[anime_id,"Name"]).lower().strip()
        nameDT2 = str(dataframe_sorted.at[anime_id,"English name"]).lower().strip()
        nameDT3 = str(dataframe_sorted.at[anime_id,"Other name"]).lower().strip()
        if name in nameDT1 or name in nameDT2 or name in nameDT3:
            result.append(build_anime_dict(anime_id,dataframe_sorted))
        if len(result)>=limit: break;
    return result


if __name__=="__main__":
    DATAFRAME = pd.read_pickle(r"Animedataset\anime_processed.pkl")
    print(searchAnime("sword", DATAFRAME,5))
