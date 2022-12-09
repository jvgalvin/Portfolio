import json

# Pull in data

with open("../data/raw/text-anonymization-benchmark/echr_dev.json") as file:
    dev_file = json.load(file)
    
with open("../data/raw/text-anonymization-benchmark/echr_train.json") as file:
    train_file = json.load(file)
       
with open("../data/raw/text-anonymization-benchmark/echr_test.json") as file:
    test_file = json.load(file)


# Parse json

dev_dict = {}

for i in range(len(dev_file)):
    
    doc_id = dev_file[i]["doc_id"]
    dev_dict[doc_id] = []
    keys_for_looping = list(dev_file[i]["annotations"].keys())
    
    for j in range(len(keys_for_looping)):
        
        inner_list = dev_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"]
        
        for k in range(len(inner_list)):
            
            if dev_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"][k]["identifier_type"] in ["DIRECT", "QUASI"]:

                start = dev_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"][k]["start_offset"]
                end = dev_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"][k]["end_offset"]
                span = [start, end]
                dev_dict[doc_id].append(span)

train_dict = {}

for i in range(len(train_file)):
    
    doc_id = train_file[i]["doc_id"]
    train_dict[doc_id] = []
    keys_for_looping = list(train_file[i]["annotations"].keys())
    
    for j in range(len(keys_for_looping)):
        
        inner_list = train_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"]
        
        for k in range(len(inner_list)):
            
            if train_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"][k]["identifier_type"] in ["DIRECT", "QUASI"]:
                
                start = train_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"][k]["start_offset"]
                end = train_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"][k]["end_offset"]
                span = [start, end]
                train_dict[doc_id].append(span)

test_dict = {}

for i in range(len(test_file)):
    
    doc_id = test_file[i]["doc_id"]
    test_dict[doc_id] = []
    keys_for_looping = list(test_file[i]["annotations"].keys())
    
    for j in range(len(keys_for_looping)):
        
        inner_list = test_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"]
        
        for k in range(len(inner_list)):
            
            if test_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"][k]["identifier_type"] in ["DIRECT", "QUASI"]:
                
                start = test_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"][k]["start_offset"]
                end = test_file[i]["annotations"][keys_for_looping[j]]["entity_mentions"][k]["end_offset"]
                span = [start, end]
                test_dict[doc_id].append(span)

# Save out

with open("../data/processed/jg_dev_masks.json", "w") as out_file:
    json.dump(dev_dict, out_file, indent = 4)

with open("../data/processed/jg_train_masks.json", "w") as out_file:
    json.dump(train_dict, out_file, indent = 4)

with open("../data/processed/jg_test_masks.json", "w") as out_file:
    json.dump(test_dict, out_file, indent = 4)