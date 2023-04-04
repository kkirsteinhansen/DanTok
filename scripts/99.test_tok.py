from transformers import AutoTokenizer
from transformers import logging as tf_logging
tf_logging.set_verbosity_error()

mlms = ['Maltehb/danish-bert-botxo', 'DDSC/roberta-base-danish', 'Maltehb/aelaectra-danish-electra-small-cased', 'vinai/bertweet-base', 'vinai/bertweet-large', 'cardiffnlp/twitter-roberta-base', 'cardiffnlp/twitter-xlm-roberta-base', 'jhu-clsp/bernice', 'Twitter/twhin-bert-large']

#import myutils

for line in open
for lm in mlms:
    text = 'Det er en test!? 💕 🥰'
    tokenizer = AutoTokenizer.from_pretrained(lm, use_fast=lm=='Twitter/twhin-bert-large')
    tokked = tokenizer.tokenize(text)

    print(lm)
    print(len(tokked), tokked)
    print()

