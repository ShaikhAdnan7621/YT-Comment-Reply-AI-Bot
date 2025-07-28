import numpy as np
import tensorflow as tf
import pickle
import re
import logging
import sys
import os
from data_preprocessing import clean_text
from modle.model import Encoder, Decoder
from utils.utils import setup_logging, setup_gpus
from utils.usage import log_interaction  # Import the new logging function
import time  # Import the time module
import psutil  # type: ignore # New import for process metrics

# Set console encoding to UTF-8
os.system('chcp 65001')
sys.stdout.reconfigure(encoding='utf-8')

# Setup logging
setup_logging()

# GPU Memory Management
setup_gpus()

# Load tokenizers and model parameters
def load_tokenizers():
    try:
        with open("data/inp_lang.pkl", "rb") as f:
            inp_tokenizer = pickle.load(f)
        with open("data/targ_lang.pkl", "rb") as f:
            targ_tokenizer = pickle.load(f)
        logging.info("Tokenizers loaded successfully")
        return inp_tokenizer, targ_tokenizer
    except Exception as e:
        logging.error(f"Error loading tokenizers: {e}")
        exit(1)

inp_tokenizer, targ_tokenizer = load_tokenizers()

# Model parameters
BATCH_SIZE = 1
embedding_dim = 256
units = 512
max_length_input = 38
max_length_target = 59
vocab_inp_size = len(inp_tokenizer.word_index) + 1
vocab_tar_size = len(targ_tokenizer.word_index) + 1

class ChatModel:
    def __init__(self):
        self.encoder = self._build_encoder()
        self.decoder = self._build_decoder()
        self._load_weights()
        
    def _build_encoder(self):
        encoder = Encoder(vocab_inp_size, embedding_dim, units, BATCH_SIZE)
        dummy_input = tf.zeros((BATCH_SIZE, max_length_input))
        encoder(dummy_input, encoder.initialize_hidden_state())
        return encoder
        
    def _build_decoder(self):
        decoder = Decoder(vocab_tar_size, embedding_dim, units, BATCH_SIZE)
        dummy_input = tf.zeros((BATCH_SIZE, 1))
        dummy_hidden = tf.zeros((BATCH_SIZE, units))
        dummy_enc_output = tf.zeros((BATCH_SIZE, max_length_input, units))
        decoder(dummy_input, dummy_hidden, dummy_enc_output)
        return decoder
        
    def _load_weights(self):
        try:
            self.encoder.load_weights("data/encoder_weights.h5")
            self.decoder.load_weights("data/decoder_weights.h5")
            logging.info("Model weights loaded successfully")
        except Exception as e:
            logging.error(f"Error loading weights: {e}")
            exit(1)
            
    def generate_response(self, sentence):
        start_time = time.time()  # Start the timer
        sentence = clean_text(sentence)
        inputs = [inp_tokenizer.word_index.get(i, 0) for i in sentence.split()]
        inputs = tf.keras.preprocessing.sequence.pad_sequences([inputs], 
                                                            maxlen=max_length_input,
                                                            padding='post')
        inputs = tf.convert_to_tensor(inputs)
        hidden = self.encoder.initialize_hidden_state()
        enc_out, enc_hidden = self.encoder(inputs, hidden)
        dec_hidden = enc_hidden
        dec_input = tf.expand_dims([targ_tokenizer.word_index['<sos>']], 0)
        result = []
        for t in range(max_length_target):
            predictions, dec_hidden, _ = self.decoder(dec_input, dec_hidden, enc_out)
            predicted_id = tf.argmax(predictions[0]).numpy()
            if targ_tokenizer.index_word[predicted_id] == '<eos>':
                break
            result.append(targ_tokenizer.index_word[predicted_id])
            dec_input = tf.expand_dims([predicted_id], 0)
        response = ' '.join(result)
        computation_time = time.time() - start_time  # Calculate the computation time
        
        proc = psutil.Process(os.getpid())
        memory_consumed = proc.memory_info().rss  # in bytes
        num_threads = proc.num_threads()
        
        return response, computation_time, memory_consumed, num_threads  # Return extra metrics

def main():
    print("\nChatbot Initialized. Type 'exit' or 'quit' to end the conversation.")
    print("-" * 50)
    
    model = ChatModel()
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                break
            if not user_input:
                continue
                
            response, computation_time, memory_consumed, num_threads = model.generate_response(user_input)
            print("Bot:", response.encode('utf-8').decode('utf-8'))
            
            # Log the interaction with all computation metrics
            log_interaction(user_input, response, computation_time, memory_consumed, num_threads)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error(f"Error during conversation: {e}")
            continue

if __name__ == "__main__":
    main()