import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import subprocess
import threading
import sys
import os
from botserver import start_server
from ytbot.commentmodel import get_comment_reply

class YouTubeBotApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("YouTube Bot Control Panel")
        self.root.geometry("1000x700")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Server control
        self.server_running = False
        self.stop_event = threading.Event()
        
        # Add password protection variable
        self.training_password = "train123"  # You can change this password
        
        # Add bot process tracking
        self.bot_process = None
        
        # Add theme tracking
        self.current_theme = "dark"
        
        # Create main container
        self.create_sidebar()
        self.create_main_area()
        
    def create_sidebar(self):
        # Sidebar frame
        sidebar = ctk.CTkFrame(self.root, width=200)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)
        sidebar.pack_propagate(False)
        
        # Logo/Title
        ctk.CTkLabel(
            sidebar,
            text="YouTube Bot",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)
        
        # Status indicators with modern switches
        self.server_switch = ctk.CTkSwitch(
            sidebar,
            text="Server Status",
            command=self.toggle_server
        )
        self.server_switch.pack(pady=10)
        
        # Add theme toggle button
        self.theme_button = ctk.CTkButton(
            sidebar,
            text="🌙 Dark Mode",
            fg_color="gray",
            command=self.toggle_theme,
            width=160
        )
        self.theme_button.pack(pady=10)
        
        # Control buttons in sidebar
        buttons_data = [
            ("⚠ Training", "#b42525", self.confirm_training)  # Changed color and command
        ]
        
        for text, color, command in buttons_data:
            ctk.CTkButton(
                sidebar,
                text=text,
                fg_color=color,
                command=command,
                width=160
            ).pack(pady=10)
            
        # Update bot button to be dynamic
        self.bot_button = ctk.CTkButton(
            sidebar,
            text="▶ Start Bot",
            fg_color="green",
            command=self.toggle_bot,
            width=160
        )
        self.bot_button.pack(pady=10)
        
    def create_main_area(self):
        # Main content area
        main = ctk.CTkFrame(self.root)
        main.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Top status bar
        status_frame = ctk.CTkFrame(main)
        status_frame.pack(fill="x", padx=5, pady=5)
        
        self.status_labels = {}
        # Added "Server" to the list of statuses.
        for name in ["Bot", "Server", "Model", "Training"]:
            self.status_labels[name] = ctk.CTkLabel(
                status_frame,
                text=f"{name}: Stopped",
                font=ctk.CTkFont(weight="bold")
            )
            self.status_labels[name].pack(side="left", padx=20)
        
        # Test comment section
        test_frame = ctk.CTkFrame(main)
        test_frame.pack(fill="x", padx=5, pady=10)
        
        ctk.CTkLabel(
            test_frame,
            text="Test Comment",
            font=ctk.CTkFont(size=16)
        ).pack(pady=5)
        
        self.test_input = ctk.CTkTextbox(
            test_frame,
            height=100
        )
        self.test_input.pack(fill="x", padx=5, pady=5)
        
        test_btn = ctk.CTkButton(
            test_frame,
            text="🔍 Test Comment",
            command=self.test_comment
        )
        test_btn.pack(pady=5)
        
        # Log section
        log_frame = ctk.CTkFrame(main)
        log_frame.pack(fill="both", expand=True, padx=5, pady=10)
        
        ctk.CTkLabel(
            log_frame,
            text="Activity Log",
            font=ctk.CTkFont(size=16)
        ).pack(pady=5)
        
        self.log_text = ctk.CTkTextbox(
            log_frame,
            wrap="word"
        )
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
    def toggle_bot(self):
        if not self.bot_process:
            try:
                self.bot_process = subprocess.Popen([sys.executable, "main.py", "bot"])
                self.bot_button.configure(text="⏹ Stop Bot", fg_color="red")
                self.status_labels["Bot"].configure(text="Bot: Running", text_color="green")
                self.log_message("Bot started successfully")
            except Exception as e:
                self.log_message(f"Error starting bot: {str(e)}")
        else:
            try:
                self.bot_process.terminate()
                self.bot_process.wait(timeout=5)  # Wait for process to end
                self.bot_process = None
                self.bot_button.configure(text="▶ Start Bot", fg_color="green")
                self.status_labels["Bot"].configure(text="Bot: Stopped", text_color="red")
                self.log_message("Bot stopped successfully")
            except Exception as e:
                self.log_message(f"Error stopping bot: {str(e)}")
                # Force kill if normal termination fails
                try:
                    self.bot_process.kill()
                    self.bot_process = None
                    self.log_message("Bot force stopped")
                except:
                    self.log_message("Failed to force stop bot")

    def toggle_server(self):
        try:
            if not self.server_running:
                self.stop_event.clear()
                self.server_thread = threading.Thread(target=start_server, args=(self.stop_event,))
                self.server_thread.daemon = True
                self.server_thread.start()
                self.server_running = True
                self.server_switch.select()
                if "Server" in self.status_labels:
                    self.status_labels["Server"].configure(text="Server: Running", text_color="green")
                self.log_message("Server started")
            else:
                self.stop_event.set()
                self.server_running = False
                self.server_switch.deselect()
                if "Server" in self.status_labels:
                    self.status_labels["Server"].configure(text="Server: Stopped", text_color="red")
                self.log_message("Server stopped")
        except Exception as e:
            self.log_message(f"Error toggling server: {str(e)}")
            if self.server_running:
                self.server_switch.select()
            else:
                self.server_switch.deselect()

    def confirm_training(self):
        # Create password dialog
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Training Confirmation")
        dialog.geometry("500x400")  # Increased size
        dialog.resizable(False, False)  # Disable resizing
        dialog.attributes('-topmost', True)  # Always on top
        
        # Center the dialog on screen
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
        
        dialog.grab_set()  # Make dialog modal
        
        # Main container frame with padding
        container = ctk.CTkFrame(dialog, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Warning label with increased size and spacing
        warning_label = ctk.CTkLabel(
            container,
            text="⚠ WARNING ⚠",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="red"
        )
        warning_label.pack(pady=(0, 10))
        
        warning_text = ctk.CTkLabel(
            container,
            text="Training will modify the model.\nThis action cannot be undone!",
            font=ctk.CTkFont(size=16),
            text_color="red"
        )
        warning_text.pack(pady=(0, 20))
        
        # Password entry with better spacing
        password_label = ctk.CTkLabel(
            container, 
            text="Enter Training Password:",
            font=ctk.CTkFont(size=14)
        )
        password_label.pack(pady=(10, 5))
        
        password_entry = ctk.CTkEntry(
            container,
            show="*",
            width=200,
            height=35
        )
        password_entry.pack(pady=(0, 15))
        
        # Confirmation checkbox with better visibility
        confirm_var = ctk.BooleanVar()
        confirm_check = ctk.CTkCheckBox(
            container,
            text="I understand the risks and consequences",
            variable=confirm_var,
            font=ctk.CTkFont(size=14)
        )
        confirm_check.pack(pady=20)
        
        # Buttons with better layout
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            fg_color="gray",
            width=120,
            height=35,
            command=dialog.destroy
        ).pack(side="left", padx=10, expand=True)
        
        ctk.CTkButton(
            button_frame,
            text="Confirm",
            fg_color="red",
            width=120,
            height=35,
            command=lambda: verify_and_start()
        ).pack(side="right", padx=10, expand=True)
        
        def verify_and_start():
            if password_entry.get() == self.training_password and confirm_var.get():
                dialog.destroy()
                self.start_training()
            else:
                self.log_message("Training access denied: Invalid password or confirmation not checked")
                password_entry.delete(0, 'end')  # Clear password field
                confirm_var.set(False)  # Uncheck confirmation
                password_entry.focus()  # Set focus back to password field

    def start_training(self):
        try:
            self.log_message("⚠ Starting model training - DO NOT INTERRUPT!")
            subprocess.Popen([sys.executable, "main.py", "train"])
            self.status_labels["Training"].configure(text="Training: Running", text_color="#ff8c00")
            self.log_message("Training process initiated")
        except Exception as e:
            self.log_message(f"Error starting training: {str(e)}")

    def test_comment(self):
        comment = self.test_input.get("1.0", "end").strip()
        if comment:
            try:
                reply = get_comment_reply(comment)
                self.log_message(f"Test Comment: {comment}")
                self.log_message(f"Model Reply: {reply}\n")
            except Exception as e:
                self.log_message(f"Error testing comment: {str(e)}")
        else:
            self.log_message("Please enter a comment to test")

    def toggle_theme(self):
        if self.current_theme == "dark":
            ctk.set_appearance_mode("light")
            self.theme_button.configure(text="☀ Light Mode")
            self.current_theme = "light"
            self.log_message("Switched to light theme")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_button.configure(text="🌙 Dark Mode")
            self.current_theme = "dark"
            self.log_message("Switched to dark theme")

    def log_message(self, message):
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        
    def run(self):
        self.root.mainloop()

def main():
    app = YouTubeBotApp()
    app.run()

if __name__ == "__main__":    main()
