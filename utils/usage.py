import logging
from datetime import datetime

def log_interaction(user_input, bot_response, computation_time, memory_consumed, num_threads):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_log_entry = f"{timestamp} - User: {user_input}\n"
    bot_log_entry = f"{timestamp} - Bot: {bot_response}\n"
    computation_log_entry = f"{timestamp} - Computation Time: {computation_time:.2f} seconds\n"
    memory_log_entry = f"{timestamp} - Memory Consumed: {memory_consumed / (1024 * 1024):.2f} MB\n"
    threads_log_entry = f"{timestamp} - Number of Threads: {num_threads}\n"
    saprator_line_log_entry = "-" * 50 + "\n"
    with open("data/usage_log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(user_log_entry)
        log_file.write(bot_log_entry)
        log_file.write(computation_log_entry)
        log_file.write(memory_log_entry)
        log_file.write(threads_log_entry)
        log_file.write(saprator_line_log_entry)
    logging.info(f"Logged interaction: {user_log_entry.strip()} | {bot_log_entry.strip()} | {computation_log_entry.strip()} | {memory_log_entry.strip()} | {threads_log_entry.strip()}")
