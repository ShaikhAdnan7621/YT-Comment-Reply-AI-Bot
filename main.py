import sys
import os

def run_bot():
    from startytbot import process_comment
    print("Starting YouTube Bot...")
    process_comment()

def run_server():
    from botserver import start_server
    import threading
    stop_event = threading.Event()
    print("Starting Server...")
    start_server(stop_event)

def run_training():
    import starttraining
    print("Starting Training...")

def run_gui():
    from gui_app import main
    print("Starting GUI...")
    main()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = sys.argv[1].lower()
        if task == "bot":
            run_bot()
        elif task == "server":
            run_server()
        elif task == "train":
            run_training()
        elif task == "gui":
            run_gui()
    else:
        run_gui()  # Default to GUI if no arguments
