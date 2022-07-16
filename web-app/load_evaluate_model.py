from transformers import BertTokenizer, BertForSequenceClassification
import pandas as pd
import numpy as np
import torch
from tqdm.notebook import tqdm
from torch.utils.data import TensorDataset
from sklearn.model_selection import train_test_split  # star
from sklearn.metrics import classification_report  # star
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from transformers import AdamW, get_linear_schedule_with_warmup
from sklearn.metrics import f1_score
import random


def load_model():
    device = torch.device('cpu')  # if using gpu, change this line accordingly.
    model = BertForSequenceClassification.from_pretrained("bert-base-uncased",
                                                          num_labels=15,
                                                          output_attentions=False,
                                                          output_hidden_states=False,
                                                          )
    model.to(device)
    model.load_state_dict(torch.load('../data/finetuned_BERT_v2_epoch_5.model', map_location=torch.device('cpu')),
                          strict=False)
    return model


# take a sentence and classify it by predicting its label using the loaded model:
def predict_text(text, model):
    device = torch.device('cpu')  # if using gpu, change this line accordingly.
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased", do_lower_case=True)
    tokenized_text = tokenizer.tokenize(text)
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    tokens_tensor = torch.tensor([indexed_tokens])
    tokens_tensor = tokens_tensor.to(device)
    with torch.no_grad():
        outputs = model(tokens_tensor)
        predictions = outputs[0]  # logits

    """ logits (https://developers.google.com/machine-learning/glossary/#logits)
    The vector of raw (non-normalized) predictions that a classification model
     generates, which is ordinarily then passed to a normalization function. 
     If the model is solving a multi-class classification problem, logits 
     typically become an input to the softmax function. The softmax function 
     then generates a vector of (normalized) probabilities with one value for each possible class."""
    """use softmax to get the probability of each label"""

    probabilities = torch.nn.functional.softmax(predictions, dim=1)
    print(probabilities.tolist())
    """get the index of the label with the highest probability"""
    predicted_index = torch.argmax(probabilities, dim=1)
    """ if it's probability is less than 0.65, return none"""
    if probabilities[0][predicted_index[0]] < 0.65:
        print(probabilities[0][predicted_index[0]])
        return probabilities, None

    predicted_label = predicted_index.item()
    return probabilities, predicted_label
