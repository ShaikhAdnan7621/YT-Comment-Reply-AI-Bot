import tensorflow as tf
import logging
import datetime

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_tensorboard():
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_dir = 'logs/gradient_tape/' + current_time
    summary_writer = tf.summary.create_file_writer(log_dir)
    logging.info(f"TensorBoard logs will be saved to {log_dir}")
    return summary_writer

def setup_gpus(gpu_number=0):
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logging.info(f"Enabled memory growth on {len(gpus)} GPU(s)")
        except RuntimeError as e:
            logging.error(e)
        try:
            tf.config.set_visible_devices(gpus[gpu_number], 'GPU')
            logging.info(f"Using GPU: {gpu_number}")
        except Exception as e:
            logging.error(f"Error selecting GPU: {e}")
    else:
        logging.info("No GPUs found, using CPU.")
