import customtkinter as ctk
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

CONTACT_FILE = "ytbot/contactinfo.txt"

def load_contact_info():
    if os.path.exists(CONTACT_FILE):
        try:
            with open(CONTACT_FILE, "r", encoding="utf-8") as f:
                line = f.readline().strip()
                parts = line.split("\t")
                if len(parts) >= 2:
                    return parts[0], parts[1]
        except Exception as e:
            print("Error loading contact info:", e)
    return "", ""

def save_contact_info(phone, whatsapp):
    try:
        with open(CONTACT_FILE, "w", encoding="utf-8") as f:
            f.write(f"{phone}\t{whatsapp}")
    except Exception as e:
        print("Error saving contact info:", e)

def show_custom_popup(comment_text, reply_text):
    def on_continue():
        nonlocal user_choice, like_selected, heart_selected, modified_reply
        user_choice = 'continue'
        like_selected = like_var.get()
        heart_selected = heart_var.get()
        modified_reply = reply_entry.get("1.0", "end").strip()
        if append_contact_var.get():
            phone = phone_entry.get().strip()
            whatsapp = whatsapp_entry.get().strip()
            modified_reply += f"\n{phone} {whatsapp}"
            save_contact_info(phone, whatsapp)
        root.destroy()

    def on_later():
        nonlocal user_choice
        user_choice = 'later'
        root.destroy()

    def on_negative():
        nonlocal user_choice
        user_choice = 'negative'
        root.destroy()

    # Default holders
    user_choice = None
    like_selected = False
    heart_selected = False
    modified_reply = reply_text

    default_phone, default_whatsapp = load_contact_info()

    # Window
    root = ctk.CTk()
    root.title("💬 AI Comment Assistant")
    root.geometry("500x570")
    root.resizable(False, False)

    # CENTER the popup:
    root.update_idletasks()
    window_width = 500
    window_height = 570
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # ALWAYS ON TOP:
    root.attributes('-topmost', True)

    # Header
    header_text = "💬  AI Comment Assistant"
    sub_text = "Review and Edit Model's Reply"
    ctk.CTkLabel(root, text=header_text, font=("Arial Rounded MT Bold", 16)).pack(pady=(12, 2))
    ctk.CTkLabel(root, text=sub_text, font=("Arial", 12), text_color="#555").pack(pady=(0, 8))

    # Comment
    ctk.CTkLabel(root, text="Comment:", anchor="w").pack(padx=15, anchor="w")
    comment_box = ctk.CTkTextbox(root, width=460, height=40, font=("Arial", 12))
    comment_box.insert("0.0", comment_text)
    comment_box.configure(state="disabled")
    comment_box.pack(padx=15, pady=5)

    # Reply
    ctk.CTkLabel(root, text="Model's Reply (Editable):", anchor="w").pack(padx=15, pady=(8, 0), anchor="w")
    reply_entry = ctk.CTkTextbox(root, width=460, height=70, font=("Arial", 12))
    reply_entry.insert("0.0", reply_text)
    reply_entry.pack(padx=15, pady=5)

    # Like & Heart
    option_frame = ctk.CTkFrame(root, fg_color="transparent")
    option_frame.pack(padx=15, pady=(5, 8), anchor="w")

    like_var = ctk.BooleanVar()
    heart_var = ctk.BooleanVar()

    ctk.CTkCheckBox(option_frame, text="👍 Like", variable=like_var).grid(row=0, column=0, padx=5, pady=5)
    ctk.CTkCheckBox(option_frame, text="❤️ Heart", variable=heart_var).grid(row=0, column=1, padx=5, pady=5)

    # Contact Info Frame
    contact_frame = ctk.CTkFrame(root, width=460, fg_color="#f1f2f6", corner_radius=8)
    contact_frame.pack(padx=15, pady=(5, 10))

    append_contact_var = ctk.BooleanVar(value=True)
    ctk.CTkCheckBox(contact_frame, text="Append contact info", variable=append_contact_var).pack(anchor="w", padx=10, pady=(8, 2))

    ctk.CTkLabel(contact_frame, text="Phone:", anchor="w").pack(anchor="w", padx=10)
    phone_entry = ctk.CTkEntry(contact_frame, width=430)
    phone_entry.insert(0, default_phone)
    phone_entry.pack(padx=10, pady=(0, 5))

    ctk.CTkLabel(contact_frame, text="WhatsApp:", anchor="w").pack(anchor="w", padx=10)
    whatsapp_entry = ctk.CTkEntry(contact_frame, width=430)
    whatsapp_entry.insert(0, default_whatsapp)
    whatsapp_entry.pack(padx=10, pady=(0, 8))

    # Buttons
    btn_frame = ctk.CTkFrame(root, fg_color="transparent")
    btn_frame.pack(pady=10)

    ctk.CTkButton(
        btn_frame, text="✅  Send Reply", width=140, height=35,
        font=("Arial", 12, "bold"),
        command=on_continue
    ).grid(row=0, column=0, padx=8)

    ctk.CTkButton(
        btn_frame, text="⏳  Review Later", width=140, height=35,
        font=("Arial", 12, "bold"),
        command=on_later
    ).grid(row=0, column=1, padx=8)

    ctk.CTkButton(
        btn_frame, text="❌  Reject", width=120, height=35,
        fg_color="#e74c3c", hover_color="#c0392b",
        font=("Arial", 12, "bold"),
        command=on_negative
    ).grid(row=0, column=2, padx=8)

    root.mainloop()

    return user_choice, like_selected, heart_selected, modified_reply
