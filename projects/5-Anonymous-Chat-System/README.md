# 🗨️ Anonymous Chat System

A **Flask-based real-time anonymous chat system** where users can:  
✅ **Join public or private chat rooms**  
✅ **Create new chat rooms**  
✅ **Leave rooms anytime**  
✅ **Chat anonymously with other users** in real-time  

This project is useful for creating temporary, private, or public chat rooms where no user identity is revealed.

---

## 🚀 Features
- 🔹 **Anonymous chatting** – No login or signup required  
- 🔹 **Room-based communication** – Users can create or join different chat rooms  
- 🔹 **Real-time messaging** (powered by Flask + SocketIO)  
- 🔹 **Easy to use interface** – Simple and lightweight  
- 🔹 **Join/Leave notifications** for better interaction  

---

## 🛠️ Tech Stack
- **Backend**: Flask (Python)  
- **Real-time Communication**: Flask-SocketIO  
- **Frontend**: HTML, CSS, JavaScript (Bootstrap for styling)  

---

## 📸 Screenshot

<img width="1365" height="624" alt="image" src="https://github.com/user-attachments/assets/4728a7b2-bdc6-422f-8200-55ca89b3a871" />

<img width="1358" height="625" alt="image" src="https://github.com/user-attachments/assets/52a76b30-6e01-428f-aabd-b33e5beecc3a" />

<img width="1364" height="618" alt="image" src="https://github.com/user-attachments/assets/8e3cdf5a-262a-40c2-af27-96c28b82e7cb" />

---

## 📂 Project Structure
```
anonymous_chat/
│
├── app.py                # Main Flask application
├── templates/
│   ├── index.html        # Home page to join or create rooms
│   ├── chat.html         # Chat room interface
│
├── static/
│   ├── style.css         # Custom styles
│   └── script.js         # SocketIO chat logic
│
└── requirements.txt      # Project dependencies
```

---

## ⚡ Installation & Running

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/anonymous_chat.git
cd anonymous_chat
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the app
```bash
python app.py
```

### 4️⃣ Open in browser  
Go to: **`http://127.0.0.1:5000`**

---

## 📝 Usage
1. **Enter a nickname (optional)** and **choose a room** or **create a new one**  
2. Start chatting anonymously  
3. Leave the room anytime  

---

## 🎯 Future Improvements
- ✅ Add private messaging  
- ✅ Add end-to-end encryption  
- ✅ Add user list for active participants  

---

## 📜 License
This project is licensed under the **MIT License** – free to use and modify.

