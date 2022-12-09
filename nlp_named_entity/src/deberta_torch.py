import tokenizers
import transformers
from transformers import AdamW
from transformers import get_linear_schedule_with_warmup
from transformers import AutoTokenizer, AutoModel, AutoConfig
from transformers import DebertaV2TokenizerFast

from tqdm.auto import tqdm

import sentencepiece
import torch
import torch.nn as nn
import torch.nn.functional as F
import json
import numpy as np
from tqdm import tqdm
from sklearn import model_selection
from transformers import AdamW
from transformers import get_linear_schedule_with_warmup

VERSION = 'v1'
MAX_LEN = 768
TRAIN_BATCH_SIZE = 4#32
VALID_BATCH_SIZE = 2#8
EPOCHS = 10
BASE_MODEL = 'microsoft/deberta-v3-large'
#BASE_MODEL = 'microsoft/deberta-v3-small'

MODEL_PATH = "model_" + BASE_MODEL.replace('/','_') + "_" + VERSION + ".bin"

TOKENIZER = DebertaV2TokenizerFast.from_pretrained(BASE_MODEL)

DEV_FILE = "./data/raw/text-anonymization-benchmark/echr_dev.json"
TRAINING_FILE = "./data/raw/text-anonymization-benchmark/echr_train.json"
TEST_FILE = "./data/raw/text-anonymization-benchmark/echr_test.json"

DEV_MASKS_FILE =    "./data/processed/jg_dev_masks.json"
TRAIN_MASKS_FILE =  "./data/processed/jg_train_masks.json"
TEST_MASKS_FILE =   "./data/processed/jg_test_masks.json"

class EntityDataset:
    def __init__(self, texts, ids, labels, offsets, masks):
        # ids: [[    0,  4454,  4571,  1691, 12435, 50118, ..., 4, 2], [0, 50118,   133,   403, 19575,    11,    41, ..., 2]]
        # texts - original texts
        # offsets - mapping of tokens to text 
        # labels: is token an identifier: [[0,0,0,0,1,1,0,0, ...,], [0,0,1,0,0,...]]
        self.texts = texts
        self.ids = ids
        self.offsets = offsets
        self.labels = labels
        self.masks = masks
    
    def __len__(self):
        return len(self.ids)
    
    def __getitem__(self, item):
        ids = self.ids[item]
        masks = self.masks[item]
        
        target_labels =self.labels[item]

        if len(target_labels) < MAX_LEN:
            target_labels = np.pad(target_labels, (0,MAX_LEN-target_labels.size),'constant', constant_values=(0))
        return {
            "ids": torch.tensor(ids, dtype=torch.long),
            "masks": torch.tensor(masks, dtype=torch.long),
            "labels": torch.tensor(target_labels, dtype=torch.float32),
        }
    #for debugging
    def printItem(i):
        masked_doc_text=''
        for token, offset, label in zip(tokens, offsets, labels):
            if label == 1:
                #masked_doc_text.append("[MASK]")
                str="*" + texts[offset[0]:offset[1]] +"*"        
                masked_doc_text.append(str)
            else:
                masked_doc_text.append(texts[offset[0]:offset[1]])
        print(masked_doc_text)

def train_fn(data_loader, model, optimizer, device, scheduler):
    model.train()
    final_loss = 0
    for data in tqdm(data_loader, total=len(data_loader)):
        for k, v in data.items():
            data[k] = v.to(device)
        optimizer.zero_grad()
        _, loss = model(**data)
        loss.backward()
        optimizer.step()
        scheduler.step()
        final_loss += loss.item()
    return final_loss / len(data_loader)

def eval_fn(data_loader, model, device):
    model.eval()
    final_loss = 0
    for data in tqdm(data_loader, total=len(data_loader)):
        for k, v in data.items():
            data[k] = v.to(device)
        _, loss = model(**data)
        final_loss += loss.item()
    return final_loss / len(data_loader)

def loss_fn(out_logits, target, mask):
    lfn = nn.BCELoss()
    #lfn = nn.CrossEntropyLoss()
    #active_loss = mask.view(-1) == 1
    #count = torch.count_nonzero(mask).item()
    #active_logits = out_logits.view(-1)
    #active_labels = torch.where(
    #    active_loss,
    #    target.view(-1),
    #    torch.tensor(lfn.ignore_index).type_as(target)
    #)
    #need these to be the same dimension
    
    #for BCE
    m = nn.Sigmoid()
    #loss = lfn(m(out_logits), target)
    #flattened = out_logits.view(-1)
    #sum_embeddings = torch.sum(out_logits, -1)
    #sum_embeddings.sum(out_logits, 2)
    #sum_embeddings = sum_embeddings.divide(out_logits.shape[-1])
    loss = lfn(m(out_logits), target)
    return loss




class MeanPooling(nn.Module):
    def __init__(self):
        super(MeanPooling, self).__init__()
        
    def forward(self, last_hidden_state, labels, attention_mask):
        #last_hidden_state.shape = [|b|,768,1024].  For deberta-small: [|b|,768,768]
        #attention_mask = [[1,1,1,1... 1,0,0,0]].  attention_mask.shape = [1,768].  For deberta-small = [768, 32]
        #desired output shape: [|b|, 768]
        #unsqueeze to add 1 dim, then duplicate in dimension to match the second hidden state dim (768)
        #tt_mask = attention_mask.unsqueeze(-1)
        #input_mask_expanded = attention_mask.unsqueeze(-1).expand(last_hidden_state.shape[1]).float()  
        #sum the hidden state tensor along the 2 dimension (1024)
        
        #for large:
        #sum_embeddings = torch.sum(last_hidden_state, 2)   
        
        #for small:
        sum_embeddings = torch.sum(last_hidden_state, 2)   
        
        
        #for small model:
        #attention_mask = torch.sum(attention_mask, 0)  
        
        sum_embeddings = torch.mul(sum_embeddings, attention_mask)
        #for large
        #sum_mask = attention_mask.sum(1)
        #sum_mask = attention_mask
        #sum_mask = torch.clamp(sum_mask, min=1e-9)
        
        
        mean_embeddings = sum_embeddings / last_hidden_state.shape[2]
        return mean_embeddings

class EntityModel(nn.Module):
    
    def __init__(self):
        super(EntityModel, self).__init__()
        #full config
        #https://huggingface.co/docs/transformers/model_doc/deberta-v2
        self.config = AutoConfig.from_pretrained(BASE_MODEL, return_dict=True)
        self.m = AutoModel.from_pretrained(BASE_MODEL, config=self.config) 
        self.mpool = MeanPooling()
    
    def forward(self, ids, masks, labels):
        
        output = self.m(ids, attention_mask=masks)
        mpool = self.mpool(output.last_hidden_state, labels, masks)

        loss_labels = loss_fn(mpool, labels, masks)        
        return labels, loss_labels

# Function used to label data
def label_tokens(toks, offs, spans_to_mask):
    """Args: 
            toks - list of token id's
            offs - list of char offsets for each token
       Returns:
            label_list - 0 for non_mask, 1 for mask"""
    
    label_list = []
    mapping_list = []    
    # Map token_ids back to string    
    for token, pos in zip(toks, offs):
        mapping_list.append([token, pos[0], pos[1]])
    
    # Determine if each token should be masked
    spans_to_mask.sort(key=lambda tup: tup[0]) #order spans, ascending
    
    j=0
    for i in range(len(mapping_list)):
        temp_list = []
        stop=False        
        while not stop and j < len(spans_to_mask):            
            if (mapping_list[i][1] >= spans_to_mask[j][0]) and (mapping_list[i][2] <= spans_to_mask[j][1]):
                temp_list.append(1)
            else:
                temp_list.append(0)           

            # Since spans and mapping_list are ordered, break to allow it to catch up
            if(spans_to_mask[j][1] > mapping_list[i][2]):
                stop=True
            else:
                j = j+1
            
        if sum(temp_list) >= 1:
            label_list.append(1)
        else:
            label_list.append(0)
    return label_list  

def process_data(data_path, masks_path):
    with open(data_path) as file:
        file = json.load(file)

    with open(masks_path) as masks_file:
        train_masks = json.load(masks_file)

    text = []
    tokens = []
    offsets = []
    labels = []
    masks = []

    for i in range(len(file)):
        doc_id = file[i]["doc_id"]
        spans_to_mask = train_masks[doc_id]
        spans_to_mask = list({tuple(x) for x in spans_to_mask}) # Make spans unique
        doc_text = file[i]["text"]
        tok_tensor = TOKENIZER.encode_plus(
            doc_text,
            add_special_tokens=True,            
            max_length=MAX_LEN,
            truncation=True,                #Truncate at MAX_LEN for now.  Can try setting MAX_LEN to the longest text.
            padding='max_length',
            return_tensors='pt',            #pytorch tensors
            return_offsets_mapping = True
        )
        
        #TOKENIZER(doc_text, return_tensors="tf", truncation=True, padding=True, return_offsets_mapping=True)
        doc_tokens = tok_tensor["input_ids"].numpy()[0]
        doc_offsets = tok_tensor["offset_mapping"].numpy()[0]
        masks_ = tok_tensor["attention_mask"].numpy()[0]
       
        labels.append(label_tokens(doc_tokens, doc_offsets, spans_to_mask))
        masks.append(masks_)
        tokens.append(doc_tokens)
        offsets.append(doc_offsets)
        text.append(doc_text)
  
    return text, tokens, labels, offsets, masks


if __name__ == "__main__":
    
    testPredictRun=True

    if testPredictRun:
        single_doc = """
        The case originated in an application (no. 40593/04) against the Republic of Turkey lodged with the Court under Article 34 of the Convention for the Protection of Human Rights and Fundamental Freedoms (“the Convention”) by a Turkish national, Mr Cengiz Polat (“the applicant”), on 15 October 2004.
        """
        tok_tensor = TOKENIZER.encode_plus(
            single_doc,
            add_special_tokens=True,            
            max_length=MAX_LEN,
            truncation=True,                #Truncate at MAX_LEN for now.  Can try setting MAX_LEN to the longest text.
            padding='max_length',
            return_tensors='pt',
            return_offsets_mapping = True
        )
        ids = tok_tensor["input_ids"].numpy()[0]
        #ids = tok_tensor.input_ids.flatten()
        #mask = tok_tensor.attention_mask

        test_dataset = EntityDataset(
            texts=[single_doc], 
            ids=[ids],        
            labels = [np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])],
            offsets = [tok_tensor["offset_mapping"].numpy()[0]],
            masks = [tok_tensor["attention_mask"].numpy()[0]]
        )

        device =  torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = EntityModel()
        #model.load_state_dict(torch.load(MODEL_PATH))
        #model.load_state_dict(torch.load(model))
        model.to(device)

        with torch.no_grad():
            data = test_dataset[0]
            for k,v in data.items():
                data[k] = v.to(device).unsqueeze(0)
            #ids_test = data.get('ids')
            #ids_size = ids_test.size()
            
            _, loss = model(**data)
            #TODO: work out the loss function and evaluation here
            #labels, loss_labels = model(**data)

    texts, tokens, labels, offsets, masks = process_data(TRAINING_FILE, TRAIN_MASKS_FILE)

    #Split train into train and test.  0.9/0.1 split
    (
        train_texts,
        test_texts,
        train_tokens,
        test_tokens,
        train_labels,
        test_labels,
        train_offsets,
        test_offsets,
        train_masks,
        test_masks
    ) = model_selection.train_test_split(texts, tokens, labels, offsets, masks, random_state=42, test_size=0.1)

    train_dataset = EntityDataset(
        texts=train_texts, ids=train_tokens, labels=train_labels, offsets=train_offsets, masks=train_masks
    )
    test_dataset = EntityDataset(
        texts=test_texts, ids=test_tokens, labels=test_labels, offsets=test_offsets, masks=test_masks
    )

    texts, tokens, labels, offsets, masks = process_data(DEV_FILE, DEV_MASKS_FILE)
    dev_dataset = EntityDataset(
        texts=texts, ids=tokens, labels=labels, offsets=offsets, masks=masks
    )
    dev_data_loader = torch.utils.data.DataLoader(
        dev_dataset, batch_size=TRAIN_BATCH_SIZE, num_workers=4
    )

    train_data_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=TRAIN_BATCH_SIZE, num_workers=4
    )

    texts, tokens, labels, offsets, masks = process_data(TEST_FILE, TEST_MASKS_FILE)
    valid_dataset = EntityDataset(
        texts=texts, ids=tokens, labels=labels, offsets=offsets, masks=masks
    )

    valid_data_loader = torch.utils.data.DataLoader(
        valid_dataset, batch_size=VALID_BATCH_SIZE, num_workers=1
    )

    device =  torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    model = EntityModel()
    model.to(device)

    param_optimizer = list(model.named_parameters())
    no_decay = ["bias", "LayerNorm.bias", "LayerNorm.weight"]
    optimizer_parameters = [
        {
            "params": [
                p for n, p in param_optimizer if not any(nd in n for nd in no_decay)
            ],
            "weight_decay": 0.001,
        },
        {
            "params": [
                p for n, p in param_optimizer if any(nd in n for nd in no_decay)
            ],
            "weight_decay": 0.0,
        },
    ]

#    num_train_steps = int(len(train_texts) / TRAIN_BATCH_SIZE * EPOCHS)
    num_train_steps = int(len(dev_dataset.texts)) / TRAIN_BATCH_SIZE * EPOCHS
    optimizer = AdamW(optimizer_parameters, lr=3e-5)
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=0, num_training_steps=num_train_steps
    )

    best_loss = np.inf
    for epoch in range(EPOCHS):
        train_loss = train_fn(dev_data_loader, model, optimizer, device, scheduler)
        test_loss = eval_fn(valid_data_loader, model, device)
        print(f"Train Loss = {train_loss} Valid Loss = {test_loss}")
        if test_loss < best_loss:
            torch.save(model.state_dict(), MODEL_PATH)
            best_loss = test_loss