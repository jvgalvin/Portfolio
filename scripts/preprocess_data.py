import json
import pandas as pd

f = open("/Users/johngalvin/Desktop/GitHub/prompt_engineering/data/raw/labeled.json", "r")
file = json.load(f)

summaries = []
dialogues = []

for i in range(len(file)):
    
    summaries.append(file[i]["summary"])
    dialogues.append(file[i]["dialogue"])

cleaned_dialogues = []

for i in range(len(dialogues)):
    newstr = dialogues[i].replace("\r\n", "    ")
    cleaned_dialogues.append(newstr)

df = pd.DataFrame()
df["dialogue"] = cleaned_dialogues
df["summary"] = summaries

df.to_csv("../data/processed/processed.csv", index=False)