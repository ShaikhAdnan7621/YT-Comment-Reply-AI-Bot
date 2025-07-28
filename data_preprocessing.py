import pandas as pd
import re
import logging
import time
import unicodedata

def load_dataset(file_path):
    start_time = time.time()
    comments = []
    replies = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                comments.append(parts[0])
                replies.append(parts[1])
            else:
                logging.warning(f"Skipping line: {line.strip()}")
    data = pd.DataFrame({"comment": comments, "reply": replies})
    logging.info(f"Dataset loaded in {time.time() - start_time:.2f} seconds")
    return data

def clean_text(text):
    """Clean and normalize input text while preserving Hindi matras"""
    text = text.lower().strip()
    text = re.sub(r'[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return f"<sos> {text} <eos>"

def preprocess_data(data):
    start_time = time.time()
    data["comment"] = data.comment.apply(clean_text)
    data["reply"] = data.reply.apply(clean_text)
    logging.info(f"Data cleaned in {time.time() - start_time:.2f} seconds")
    return data
