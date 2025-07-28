import pyautogui
import time
import pyperclip
import os
from ytbot.commentmodel import get_comment_reply
from ytbot.popupwindow import show_custom_popup

# Ensure the dataset directory exists
DATASET_DIR = "data/newdataset"
if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)

COMMENTS_FILE = os.path.join(DATASET_DIR, "comments.txt")

# ----------- Initial Navigation -----------
pyautogui.moveTo(139, 143, duration=0.5)
pyautogui.click()
print("Clicked First Button")
time.sleep(1.5)

pyautogui.moveTo(135, 667, duration=0.5)
pyautogui.click()
print("Clicked Second Button")
time.sleep(1.5)

# ----------- Main Process Function -----------
def process_comment():
    # --- Apply Filter Buttons ---
    pyautogui.moveTo(495, 428, duration=0.5)
    pyautogui.click()
    time.sleep(1)

    pyautogui.moveTo(534, 511, duration=0.5)
    pyautogui.click()
    time.sleep(1)

    pyautogui.moveTo(621, 663, duration=0.5)
    pyautogui.click()
    time.sleep(2)

    # --- Process Comment ---
    pyautogui.moveTo(556, 526, duration=0.5)
    pyautogui.click(clicks=3, interval=0.25)
    time.sleep(0.5)

    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)

    comment_text = pyperclip.paste()
    print("Comment Text:", comment_text)

    # Get model reply (this reply is before appending contact info)
    model_reply = get_comment_reply(comment_text)
    print("Model Reply:", model_reply)

    # Show popup and get decisions; final_reply may have contact info appended if chosen
    decision, like_flag, heart_flag, final_reply = show_custom_popup(comment_text, model_reply)
    print(f"Popup Decision: {decision}, Like: {like_flag}, Heart: {heart_flag}")
    print(f"Final Reply: {final_reply}")

    status = "normal"  # default status

    if decision == 'continue':
        # Focus reply section and bring up the reply text box
        pyautogui.moveTo(533, 558, duration=0.5)
        pyautogui.click()
        time.sleep(1)

        pyautogui.moveTo(542, 645, duration=0.5)
        pyautogui.click()
        time.sleep(0.5)

        # Perform navigation with Shift+Tab, Tab, etc. (as in your previous code)
        for _ in range(5):
            pyautogui.hotkey('shift', 'tab')
            time.sleep(0.1)
        if like_flag:
            pyautogui.press('space')
            print("Liked the comment")
            time.sleep(0.3)
        for _ in range(2):
            pyautogui.press('tab')
            time.sleep(0.1)
        if heart_flag:
            pyautogui.press('space')
            print("Hearted the comment")
            time.sleep(0.3)
        for _ in range(3):
            pyautogui.press('tab')
            time.sleep(0.1)

        # Paste the final reply (with contact info appended if applicable)
        pyperclip.copy(final_reply)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)

        for _ in range(2):
            pyautogui.press('tab')
            time.sleep(0.1)

        pyautogui.press('enter')
        print("Reply sent")
        time.sleep(2)

    elif decision == 'later':
        print("Action postponed.")
        status = "later"

    elif decision == 'negative':
        print("Comment marked as negative.")
        status = "negative"
        pyautogui.moveTo(533, 558, duration=0.5)
        pyautogui.click()
        time.sleep(1)
        for _ in range(2):
            pyautogui.hotkey('shift', 'tab')
            time.sleep(0.1)
        pyautogui.press('space')
        time.sleep(0.5)
        for _ in range(1):
            pyautogui.press('tab')
            time.sleep(0.1)
        pyautogui.press('space')
        print("Negative action performed.")
        time.sleep(1)
    else:
        print("No action taken.")
        status = "unknown"

    # After processing, log the comment details to COMMENTS_FILE.
    # We store: original comment, model reply (without appended contact info), and status.
    try:
        with open(COMMENTS_FILE, "a", encoding="utf-8") as f:
            f.write(f"{comment_text}\t{model_reply}\t{status}\n")
        print("Comment details logged.")
    except Exception as e:
        print("Error logging comment:", e)

    # Refresh the page for next comment (only if continue action was taken)
    if decision == 'continue':
        pyautogui.hotkey('ctrl', 'r')
        time.sleep(5)

# ----------- Main Loop -----------
for i in range(10):
    print(f"\n--- Iteration {i+1} ---\n")
    process_comment()
