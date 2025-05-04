# import customtkinter as ctk
# import requests

# #Set theme and appearance
# ctk.set_appearance_mode("light")  # Options: "dark", "light", "system"
# ctk.set_default_color_theme("blue")

# import requests

# def get_ai_response(user_input):
#     try:
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": "phi",  # or mistral, phi, etc.
#                 "prompt": user_input,
#                 "stream": False
#             }
#         )
#         if response.status_code == 200:
#             return response.json()['response'].strip()
#         else:
#             return "⚠️ AI error: Could not get a response."
#     except Exception as e:
#         return f"❌ Connection error: {e}"


# def send_message():
#     user_input = input_box.get()
#     if user_input.strip() == "":
#         return
#     chat_log.configure(state="normal")
#     chat_log.insert("end", f"You: {user_input}\n")
#     input_box.delete(0, "end")

#     response = get_ai_response(user_input)
#     chat_log.insert("end", f"AI: {response}\n\n")
#     chat_log.configure(state="disabled")
#     chat_log.see("end")

# # Create main window
# app = ctk.CTk()
# app.title("🧠 Secret Door AI")
# app.geometry("600x600")
# app.resizable(False, False)

# # Chat log (read-only text box)
# chat_log = ctk.CTkTextbox(app, width=560, height=450, corner_radius=12)
# chat_log.pack(padx=20, pady=(20,10))
# chat_log.insert("end", "🔐 Welcome to the Secret Door.\n")
# chat_log.configure(state="disabled")

# # Input box
# input_box = ctk.CTkEntry(app, placeholder_text="Type your message here...", width=460, height=40, corner_radius=10)
# input_box.pack(padx=20, pady=(0, 10), side="left")
# input_box.bind("<Return>", lambda event: send_message())

# # Send button
# send_button = ctk.CTkButton(app, text="Send", width=100, command=send_message)
# send_button.pack(pady=(0, 10), padx=(0, 20), side="right")

# app.mainloop()

import customtkinter as ctk
import requests
import json
import os
from PIL import Image, ImageTk

# === Setup ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Define file paths for chat history
CHAT_DIR = "chats"
os.makedirs(CHAT_DIR, exist_ok=True)

# AI Function ===
def get_ai_response(user_input):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "nyra",
                "prompt": user_input,
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json()['response'].strip()
        else:
            return "⚠️ AI error: Could not get a response."
    except Exception as e:
        return f"❌ Connection error: {e}"

# Send Message ===
def send_message():
    user_input = input_box.get()
    if user_input.strip() == "":
        return

    # Insert user message into the chat log
    chat_log.configure(state="normal")
    chat_log.insert("end", f"\n🧍 You:\n{user_input}\n\n", "user")
    input_box.delete(0, "end")

    # Get response from AI
    response = get_ai_response(user_input)
    chat_log.insert("end", f"🤖 Nyra:\n{response}\n\n", "bot")
    chat_log.configure(state="disabled")
    chat_log.see("end")

    # Save chat history
    save_chat_history(current_chat_name, user_input, response)

# === Chat History Management ===
def load_chat_history(chat_name):
    chat_file = os.path.join(CHAT_DIR, f"{chat_name}.json")
    if os.path.exists(chat_file):
        with open(chat_file, "r") as f:
            chat_data = json.load(f)
            return chat_data['messages']
    return []

def save_chat_history(chat_name, user_message, ai_response):
    chat_file = os.path.join(CHAT_DIR, f"{chat_name}.json")
    chat_data = {
        "chat_name": chat_name,
        "messages": [{"role": "user", "message": user_message}, {"role": "bot", "message": ai_response}]
    }
    if os.path.exists(chat_file):
        with open(chat_file, "r") as f:
            existing_data = json.load(f)
            existing_data['messages'].append({"role": "user", "message": user_message})
            existing_data['messages'].append({"role": "bot", "message": ai_response})
            chat_data = existing_data
    with open(chat_file, "w") as f:
        json.dump(chat_data, f, indent=4)

def delete_chat(chat_name):
    chat_file = os.path.join(CHAT_DIR, f"{chat_name}.json")
    if os.path.exists(chat_file):
        os.remove(chat_file)

# === UI Setup ===
app = ctk.CTk()
app.title("🤖 Nyra AI Assistant")
app.geometry("1000x650")
app.resizable(True, True)

# === Layout ===
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

sidebar = ctk.CTkFrame(main_frame, width=200, corner_radius=12)
sidebar.pack(side="left", fill="y", padx=(0, 10))

content = ctk.CTkFrame(main_frame, corner_radius=12)
content.pack(side="left", fill="both", expand=True)

# === Sidebar ===
chat_list_label = ctk.CTkLabel(sidebar, text="💬 Chats", font=("Segoe UI", 14, "bold"))
chat_list_label.pack(pady=10)

chat_listbox = ctk.CTkTextbox(sidebar, width=180, height=500, corner_radius=8)
chat_listbox.configure(state="disabled")
chat_listbox.pack(pady=10, padx=10)

def update_chat_list():
    chat_listbox.configure(state="normal")
    chat_listbox.delete(1.0, "end")
    for chat_file in os.listdir(CHAT_DIR):
        if chat_file.endswith(".json"):
            chat_name = chat_file[:-5]
            chat_listbox.insert("end", f"{chat_name}\n")
    chat_listbox.insert("end", "+ New Chat\n")
    chat_listbox.configure(state="disabled")

# === Top Logo & Title ===
title_frame = ctk.CTkFrame(content)
title_frame.pack(fill="x", padx=10, pady=(10, 0))

# Load AI Logo (Use your own rounded PNG logo)
try:
    img = Image.open("nyra_logo.png")  # 🔁 Replace with your own logo if needed
    img = img.resize((40, 40), Image.ANTIALIAS)
    logo_img = ImageTk.PhotoImage(img)
    logo = ctk.CTkLabel(title_frame, image=logo_img, text="")
    logo.pack(side="left", padx=10)
except:
    logo = ctk.CTkLabel(title_frame, text="🤖", font=("Segoe UI", 30))
    logo.pack(side="left", padx=10)

title_label = ctk.CTkLabel(title_frame, text="Nyra - Your Secret AI", font=("Segoe UI", 24, "bold"))
title_label.pack(side="left")

# === Chat Log ===
chat_log = ctk.CTkTextbox(content, width=600, height=400, corner_radius=12, wrap="word")
chat_log.tag_config("user", spacing1=4, spacing3=10)
chat_log.tag_config("bot", spacing1=4, spacing3=15)
chat_log.insert("end", "🔐 Welcome to Nyra. Start your private AI conversation.\n\n")
chat_log.configure(state="disabled")
chat_log.pack(padx=20, pady=(10, 5), fill="both", expand=True)

# === Input Section ===
input_frame = ctk.CTkFrame(content)
input_frame.pack(fill="x", padx=20, pady=(0, 10))

input_box = ctk.CTkEntry(input_frame, placeholder_text="Type your message here...", height=40, corner_radius=10)
input_box.pack(side="left", padx=(0, 10), pady=10, fill="x", expand=True)
input_box.bind("<Return>", lambda event: send_message())

send_button = ctk.CTkButton(input_frame, text="Send", width=100, command=send_message)
send_button.pack(side="right", pady=10)

# === Chat Listbox Interaction ===
def select_chat(event):
    global current_chat_name
    # Get clicked text (line of text where the click happened)
    selected_chat = chat_listbox.get("current linestart", "current lineend").strip()

    if selected_chat == "+ New Chat":  # Handle New Chat Creation
        current_chat_name = f"Chat_{len(os.listdir(CHAT_DIR)) + 1}"
        save_chat_history(current_chat_name, "", "")  # Initialize new chat file
        update_chat_list()
    elif selected_chat != "":
        current_chat_name = selected_chat
        messages = load_chat_history(current_chat_name)
        chat_log.configure(state="normal")
        chat_log.delete(1.0, "end")
        for message in messages:
            role = "user" if message["role"] == "user" else "bot"
            chat_log.insert("end", f"\n{message['role']}: {message['message']}\n", role)
        chat_log.configure(state="disabled")
        chat_log.see("end")

def delete_chat_func():
    global current_chat_name
    if current_chat_name and current_chat_name != "+ New Chat":
        delete_chat(current_chat_name)
        update_chat_list()
        chat_log.configure(state="normal")
        chat_log.delete(1.0, "end")
        chat_log.configure(state="disabled")

chat_listbox.bind("<ButtonRelease-1>", select_chat)

# === Delete Chat Button ===
delete_button = ctk.CTkButton(sidebar, text="Delete Chat", width=180, command=delete_chat_func)
delete_button.pack(pady=10)

# === Button Hover Effects ===
def on_hover(event):
    event.widget.configure(bg_color="gray")

def on_leave(event):
    event.widget.configure(bg_color="transparent")

delete_button.bind("<Enter>", on_hover)
delete_button.bind("<Leave>", on_leave)

# === Mouse Cursor Update ===
def update_cursor(event):
    event.widget.configure(cursor="hand2")

# Apply cursor change to clickable elements
delete_button.bind("<Enter>", update_cursor)
chat_listbox.bind("<Enter>", update_cursor)
update_chat_list()

app.mainloop()
