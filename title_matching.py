
import re 
test = "Sword Art Online: Alicization - Recollection"
test2 = "Sword Art Online"
def norm(s:str):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+",' ',s)
    return s.strip()
def is_related(title1:str, title2:str):
    words1 = norm(title1).split()
    words2 = norm(title2).split()
    max_prefix_len = 0
    for word1,word2 in zip(words1,words2):
        if word1 == word2: max_prefix_len+=1
        else: break;
    min_len = min(len(words1), len(words2))
    return max_prefix_len >= 2 and max_prefix_len >= min_len / 2

if __name__ == "__main__":
    print(is_related(test,test2))