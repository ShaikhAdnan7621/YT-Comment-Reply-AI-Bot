import logging
import pickle
import time
from sklearn.model_selection import train_test_split
import tensorflow as tf
from data_preprocessing import load_dataset, preprocess_data
from model.tokenization import tokenize
from model.model import Encoder, Decoder
from model.train import train_model
from utils.utils import setup_logging, setup_tensorboard, setup_gpus
    
# Setup logging and TensorBoard
setup_logging()
summary_writer = setup_tensorboard()

# GPU setup
setup_gpus()

# Load and preprocess dataset
data = load_dataset("data/trainingdata/ProcessedComments_export.txt")
data = preprocess_data(data)

# Tokenization
comment_list = data.comment.values.tolist()
reply_list = data.reply.values.tolist()
input_tensor, inp_tokenizer = tokenize(comment_list)
target_tensor, targ_tokenizer = tokenize(reply_list)

# Train-test split
input_tensor_train, input_tensor_val, target_tensor_train, target_tensor_val = train_test_split(
    input_tensor, target_tensor, test_size=0.2)
logging.info("Train-test split completed")

# Model parameters
BUFFER_SIZE = len(input_tensor_train)
BATCH_SIZE = 16
embedding_dim = 256
units = 512
vocab_inp_size = len(inp_tokenizer.word_index) + 1
vocab_tar_size = len(targ_tokenizer.word_index) + 1

# Prepare dataset
dataset = tf.data.Dataset.from_tensor_slices((input_tensor_train, target_tensor_train)) \
            .shuffle(BUFFER_SIZE) \
            .batch(BATCH_SIZE, drop_remainder=True) \
            .prefetch(tf.data.AUTOTUNE)
logging.info("Dataset prepared for training")

# Initialize models
encoder = Encoder(vocab_inp_size, embedding_dim, units, BATCH_SIZE)
decoder = Decoder(vocab_tar_size, embedding_dim, units, BATCH_SIZE)
logging.info("Models initialized")

# Optimizer
optimizer = tf.keras.optimizers.Adam()

# Train the model
train_model(dataset, encoder, decoder, optimizer, targ_tokenizer, summary_writer)

# Save tokenizers
start_time = time.time()
with open("data/inp_lang.pkl", "wb") as f:
    pickle.dump(inp_tokenizer, f)
with open("data/targ_lang.pkl", "wb") as f:
    pickle.dump(targ_tokenizer, f)
logging.info(f"Tokenizers saved in {time.time() - start_time:.2f} seconds")

# Save the model
start_time = time.time()
encoder.save_weights("data/encoder_weights.h5")
decoder.save_weights("data/decoder_weights.h5")
logging.info(f"Model saved in {time.time() - start_time:.2f} seconds")

# Load model later (if needed)
start_time = time.time()
encoder.load_weights("data/encoder_weights.h5")
decoder.load_weights("data/decoder_weights.h5")
logging.info(f"Model loaded successfully in {time.time() - start_time:.2f} seconds")