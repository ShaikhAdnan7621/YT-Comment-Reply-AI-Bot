import tensorflow as tf
import logging
import time
from modle.model import Encoder, Decoder
from tokenization import tokenize
from sklearn.model_selection import train_test_split

def loss_function(real, pred):
    mask = tf.math.logical_not(tf.math.equal(real, 0))
    loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True, reduction='none')
    loss_ = loss_object(real, pred)
    loss_ *= tf.cast(mask, dtype=loss_.dtype)
    return tf.reduce_mean(loss_)

@tf.function
def train_step(inp, targ, enc_hidden, encoder, decoder, optimizer, targ_tokenizer):
    loss = 0
    with tf.GradientTape() as tape:
        enc_output, enc_hidden = encoder(inp, enc_hidden)
        dec_hidden = enc_hidden
        dec_input = tf.expand_dims([targ_tokenizer.word_index['<sos>']] * inp.shape[0], 1)
        for t in range(1, targ.shape[1]):
            predictions, dec_hidden, _ = decoder(dec_input, dec_hidden, enc_output)
            loss += loss_function(targ[:, t], predictions)
            dec_input = tf.expand_dims(targ[:, t], 1)
    batch_loss = loss / int(targ.shape[1])
    variables = encoder.trainable_variables + decoder.trainable_variables
    gradients = tape.gradient(loss, variables)
    optimizer.apply_gradients(zip(gradients, variables))
    return batch_loss

def train_model(dataset, encoder, decoder, optimizer, targ_tokenizer, summary_writer, EPOCHS=40):
    for epoch in range(1, EPOCHS + 1):
        start_time_epoch = time.time()
        enc_hidden = encoder.initialize_hidden_state()
        total_loss = 0
        num_batches = 0
        
        progress_bar = tf.keras.utils.Progbar(target=len(dataset))
        
        for (batch, (inp, targ)) in enumerate(dataset):
            batch_loss = train_step(inp, targ, enc_hidden, encoder, decoder, optimizer, targ_tokenizer)
            total_loss += batch_loss
            num_batches += 1
            
            progress_bar.update(batch + 1, values=[('batch_loss', float(batch_loss))])
            
            with summary_writer.as_default():
                tf.summary.scalar('batch_loss', float(batch_loss), step=epoch * len(dataset) + batch)
            
            if batch % 100 == 0:
                current_loss = float(batch_loss.numpy())
                logging.info(f'Epoch {epoch}/{EPOCHS} - Batch {batch}/{len(dataset)} - Loss: {current_loss:.4f}')
        
        avg_loss = float(total_loss / num_batches)
        epoch_time = time.time() - start_time_epoch
        
        logging.info(
            f'\nEpoch {epoch}/{EPOCHS} Summary:\n'
            f'Average Loss: {avg_loss:.4f}\n'
            f'Time Taken: {epoch_time:.2f} seconds\n'
            f'--------------------------------'
        )
        
        with summary_writer.as_default():
            tf.summary.scalar('epoch_loss', avg_loss, step=epoch)
            tf.summary.scalar('epoch_time', epoch_time, step=epoch)
        
        time.sleep(60)
