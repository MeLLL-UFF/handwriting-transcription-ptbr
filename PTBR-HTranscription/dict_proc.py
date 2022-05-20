import re
from simhash import Simhash, SimhashIndex
import pandas as pd

## Transform a text into a features list
# @param s text to be transformed
# @return list of features from s
def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

## Read file with words in line and turn it into a dataframe
# @param ptdict_file path for words dictionary
# @return pandas dataframe with dictionary words
def dict_pt_words(ptdict_file):
    print("\nBuilding pt-br dictionary...")
    file = open(ptdict_file, 'r')
    pttext = file.read().split("\n")
    pt_dict = pd.DataFrame(pttext, columns=['a'])
    pt_dict = pt_dict.drop_duplicates(keep="first")['a']
    print("Dictionary with "+str(len(pt_dict))+" words created.")
    return pt_dict

## Build indexing structure for words from dictionary
# @param pt_dict pt-br dictionary
# @param k_sim tolerance of near words to look for
# @return SimhashIndex object with indexing words from dictionary
def dict_indexing(pt_dict, k_sim):
    print("\nBuilding indexing for dictionary words...")
    objs = [(str(k), Simhash(get_features(v))) for k, v in pt_dict.items()]
    print("Indexing for "+str(len(objs))+" words concluded.\n")
    return SimhashIndex(objs, k=int(k_sim))

## Search for words in dictionary to replace misinferred words
# @param index indexing structure for the dictionary
# @param pt_dict pt-br dictionary
# @param infered_text original text infered before replacement
# @return infered text with misinferred words replaced from dictionary
def find_similarities(index, pt_dict, infered_text):
    print("Searching for words similarities in pt-br dictionary...")
    subtext = ""
    for t in infered_text.split(" "):
        if t.lower() not in pt_dict.values:
            w = Simhash(get_features(t))
            sims = index.get_near_dups(w)
            if len(sims) > 0:
                subtext += "<" + pt_dict[int(sims[0])] + ">" + " "
                continue
            else:
                pass
        
        subtext += t
        subtext += " "

    #print("Refined text: ")
    #print(subtext, "\n")
    return subtext