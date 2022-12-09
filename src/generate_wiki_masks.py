import json

# Pull in data

with open("../data/raw/wiki-summaries/annotated_wikipedia.json") as file:
    wiki_file = json.load(file)


# Parse json

wiki_dict = {}

for i in range(len(wiki_file)):
    
    doc_id = wiki_file[i]["doc_id"]
    wiki_dict[doc_id] = []
    keys_for_looping = list(wiki_file[i]["annotations"].keys())
    
    for j in range(len(keys_for_looping)):
        
        inner_list = wiki_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"]
        
        for k in range(len(inner_list)):
            
            if wiki_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"][k]["identifier_type"] in ["DIRECT", "QUASI"]:

                start = wiki_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"][k]["start_offset"]
                end = wiki_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"][k]["end_offset"]
                span = [start, end]
                wiki_dict[doc_id].append(span)

# Save out

with open("../data/processed/wiki_masks.json", "w") as out_file:
    json.dump(wiki_dict, out_file, indent = 4)