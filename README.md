# 🤖 Nyra - Your Personal AI Assistant

Nyra is a beautiful, modern, and offline AI assistant powered by a local LLM (Large Language Model) served through [Ollama](https://ollama.com). It's designed to give you a clean and responsive user interface with chat history, multi-session management, and a personalized assistant experience.

---

## 💡 Features

- 🪄 Chat UI with smooth user/assistant formatting
- 💬 Sidebar with multi-chat support (create/delete chats)
- 🧠 Custom AI personality named **Nyra**
- 💻 100% offline - private and secure
- 🎨 Built using Python & [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

---

## 📸 Preview
![WhatsApp Image 2025-05-01 at 21 20 49_1299a92d](https://github.com/user-attachments/assets/b5d9b440-7c4a-4d40-8459-e60b1224bce9)



---

## 🧰 Requirements

- Windows OS (Tested on Windows 10/11)
- [Python 3.10+](https://www.python.org/)
- [Ollama](https://ollama.com) installed and running

---

## 🚀 Getting Started

### 1. Clone the Repository

### 2. Install Python Dependencies
  - pip install -r requirements.txt
Or manually install:
  - pip install customtkinter requests pillow
    
## 🧠 Setting Up the AI Model with Ollama
### 3. Install Ollama
  - Download and install Ollama from: https://ollama.com
    
### 4. Download the Base Model (Phi)
  -ollama pull phi
  
### 5. Create the Custom Model Named nyra

This step configures your assistant’s personality permanently.

### ⚙️ Run the following in PowerShell or CMD:

  $nyraPath = "$env:USERPROFILE\.ollama\nyra"
New-Item -ItemType Directory -Force -Path $nyraPath | Out-Null
Set-Content -Path "$nyraPath\Modelfile" -Value 'FROM phi
SYSTEM "You are Nyra, a smart assistant who never refers to yourself as GPT or OpenAI. You are friendly, helpful, and always speak clearly and kindly."'
cd $nyraPath
ollama create nyra -f Modelfile
  
  - ✅ This creates a model named nyra that behaves like a human-friendly assistant and hides any GPT/OpenAI references.

### 6. Verify the Model
  - ollama list
#### You should see something like:

  NAME           ID              SIZE      MODIFIED
nyra:latest    abc123...       1.6 GB    Just now
phi:latest     xyz456...       1.6 GB    Earlier

### 💬 Running the App

Once your model is ready:
  - python secret_ai_chat.py
    
## 🛠 Customization

  - Change the model name by editing model: "nyra" inside secret_ai_chat.py

  - Replace nyra_logo.png with your own logo (40x40 PNG recommended)

  - You can modify Nyra’s behavior by editing the Modelfile

## 🔐 Offline & Private

  - All conversations and models run entirely offline. Nothing is sent to the cloud. Your data stays with you.

