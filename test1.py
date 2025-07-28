import tensorflow as tf
import numpy as np
import time
from datetime import datetime

# GPU Memory Management
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"Using GPU: {gpus[0].name}")
    except RuntimeError as e:
        print(e)

# Model parameters
BATCH_SIZE = 64
MATRIX_SIZE = 4096  # Increased for more GPU load
NUM_LAYERS = 4

class GPUStressModel(tf.keras.Model):
    def __init__(self):
        super(GPUStressModel, self).__init__()
        self.layers_list = []
        for _ in range(NUM_LAYERS):
            self.layers_list.append(tf.keras.layers.Dense(MATRIX_SIZE, activation='relu'))
    
    def call(self, x):
        for layer in self.layers_list:
            x = layer(x)
        return x

def run_gpu_test(duration_seconds=60):
    print("\nInitializing GPU stress test...")
    print(f"Matrix size: {MATRIX_SIZE}x{MATRIX_SIZE}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Duration: {duration_seconds} seconds")
    
    # Initialize model and optimizer
    model = GPUStressModel()
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    
    start_time = time.time()
    iteration = 0
    
    try:
        while (time.time() - start_time) < duration_seconds:
            # Generate random tensors
            input_tensor = tf.random.normal([BATCH_SIZE, MATRIX_SIZE])
            target_tensor = tf.random.normal([BATCH_SIZE, MATRIX_SIZE])
            
            # Training step
            with tf.GradientTape() as tape:
                output = model(input_tensor)
                loss = tf.reduce_mean(tf.square(output - target_tensor))
                
                if iteration % 5 == 0:
                    elapsed = time.time() - start_time
                    print(f"\rIteration: {iteration:5d} | "
                          f"Time: {elapsed:6.2f}s | "
                          f"Loss: {float(loss):10.4f}", end="")
            
            # Backpropagation
            grads = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))
            iteration += 1
            
    except KeyboardInterrupt:
        print("\n\nTest stopped by user")
    
    total_time = time.time() - start_time
    print(f"\n\nTest completed:")
    print(f"Total iterations: {iteration}")
    print(f"Time elapsed: {total_time:.2f} seconds")
    print(f"Iterations per second: {iteration/total_time:.2f}")

if __name__ == "__main__":
    print("TensorFlow GPU Stress Test")
    print("==========================")
    
    try:
        duration = int(input("Enter test duration in seconds (default: 60): ") or "60")
    except ValueError:
        duration = 60
    
    run_gpu_test(duration)