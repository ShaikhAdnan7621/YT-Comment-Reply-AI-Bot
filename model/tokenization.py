import numpy as np
import tensorflow as tf
import logging
import time

def tokenize(text_list, maxlen=None):
    start_time = time.time()
    tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='')
    tokenizer.fit_on_texts(text_list)
    tensor = tokenizer.texts_to_sequences(text_list)
    if maxlen is None:
        lengths = [len(seq) for seq in tensor]
        maxlen = int(np.percentile(lengths, 95))
        logging.info(f"Using max sequence length: {maxlen}")
    tensor = tf.keras.preprocessing.sequence.pad_sequences(tensor, maxlen=maxlen, padding='post')
    logging.info(f"Tokenization completed in {time.time() - start_time:.2f} seconds")
    return tensor, tokenizer
