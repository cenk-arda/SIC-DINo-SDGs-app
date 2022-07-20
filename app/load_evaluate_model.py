from transformers import BertTokenizer, BertForSequenceClassification
import pandas as pd
import numpy as np
import torch
import tqdm
from torch.utils.data import TensorDataset


def load_model():
    device = torch.device('cpu')  # if using gpu, change this line accordingly.
    model = BertForSequenceClassification.from_pretrained("bert-base-uncased",
                                                          num_labels=15,
                                                          output_attentions=False,
                                                          output_hidden_states=False,
                                                          )
    model.to(device)
    model.load_state_dict(torch.load('data/finetuned_BERT_v2_epoch_5.model', map_location=torch.device('cpu')),
                          strict=False)
    return model


# take a sentence and classify it by predicting its label using the loaded model:
def predict_text(text, model):
    device = torch.device('cpu')  # if using gpu, change this line accordingly.
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased", do_lower_case=True)
    encoded_input = tokenizer(text, return_tensors='pt')
    encoded_input = encoded_input.to(device)
    model.eval()
    with torch.no_grad():
        outputs = model(**encoded_input)
        predictions = outputs[0]  # logits

    """ logits (https://developers.google.com/machine-learning/glossary/#logits)
    The vector of raw (non-normalized) predictions that a classification model
     generates, which is ordinarily then passed to a normalization function. 
     If the model is solving a multi-class classification problem, logits 
     typically become an input to the softmax function. The softmax function 
     then generates a vector of (normalized) probabilities with one value for each possible class."""
    """use softmax to get the probability of each label"""

    probabilities = torch.nn.functional.softmax(predictions, dim=1)
    # print(probabilities.tolist())
    """get the index of the label with the highest probability"""
    predicted_index = torch.argmax(probabilities, dim=1)
    """ if it's probability is less than 70%, return none"""
    if probabilities[0][predicted_index[0]] < 0.70:
        # print(probabilities[0][predicted_index[0]])
        return probabilities, None

    predicted_label = predicted_index.item()
    return probabilities, predicted_label
