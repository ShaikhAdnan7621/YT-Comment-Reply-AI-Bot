# commentmodel.py

import tensorflow as tf
import pickle
from data_preprocessing import clean_text
from model.model import Encoder, Decoder

# Load tokenizers
with open("data/inp_lang.pkl", "rb") as f:
    inp_tokenizer = pickle.load(f)
with open("data/targ_lang.pkl", "rb") as f:
    targ_tokenizer = pickle.load(f)

# Model parameters
BATCH_SIZE = 1
embedding_dim = 256
units = 512
max_length_input = 38
max_length_target = 59
vocab_inp_size = len(inp_tokenizer.word_index) + 1
vocab_tar_size = len(targ_tokenizer.word_index) + 1

# Build Encoder and Decoder
encoder = Encoder(vocab_inp_size, embedding_dim, units, BATCH_SIZE)
decoder = Decoder(vocab_tar_size, embedding_dim, units, BATCH_SIZE)

# Dummy forward pass to initialize
encoder(tf.zeros((BATCH_SIZE, max_length_input)), encoder.initialize_hidden_state())
decoder(tf.zeros((BATCH_SIZE, 1)), tf.zeros((BATCH_SIZE, units)), tf.zeros((BATCH_SIZE, max_length_input, units)))

# Load weights
encoder.load_weights("data/encoder_weights.h5")
decoder.load_weights("data/decoder_weights.h5")


# ---- Simple function ----

def get_comment_reply(user_input: str) -> str:
    """
    Takes user input (comment), returns model-generated reply as string.
    """
    # Preprocess input
    sentence = clean_text(user_input)
    inputs = [inp_tokenizer.word_index.get(i, 0) for i in sentence.split()]
    inputs = tf.keras.preprocessing.sequence.pad_sequences([inputs], maxlen=max_length_input, padding='post')
    inputs = tf.convert_to_tensor(inputs)

    hidden = encoder.initialize_hidden_state()
    enc_out, enc_hidden = encoder(inputs, hidden)

    dec_hidden = enc_hidden
    dec_input = tf.expand_dims([targ_tokenizer.word_index['<sos>']], 0)

    result = []

    for t in range(max_length_target):
        predictions, dec_hidden, _ = decoder(dec_input, dec_hidden, enc_out)
        predicted_id = tf.argmax(predictions[0]).numpy()
        if targ_tokenizer.index_word[predicted_id] == '<eos>':
            break
        result.append(targ_tokenizer.index_word[predicted_id])
        dec_input = tf.expand_dims([predicted_id], 0)

    return ' '.join(result)
