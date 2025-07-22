# 📝 Flask Blog System

A **full-featured blog system built with Flask** — similar to a mini WordPress!  
It supports **admin-only blog management**, **rich text editing**, **draft & scheduled posts**, and **anonymous comments**.

---

## 🚀 Features

✅ **Admin Panel** (only admin can add/edit/delete blogs)  
✅ **Rich Text Editor** (bold, italics, images, videos — CKEditor integrated)  
✅ **Draft & Scheduled Posts** (publish later automatically)  
✅ **Anonymous Comments** (anyone can comment without login)  
✅ **Latest Blogs First** (auto-sorted by timestamp)  
✅ **Secure Admin Login** (Flask-Login)  
✅ **Simple & Beautiful UI (Bootstrap 5)**

---

## 📸 Screenshots

### 🏠 Public View  
<img width="1348" height="576" alt="image" src="https://github.com/user-attachments/assets/3e277e70-c376-43f0-900c-01fbd52ee457" />


### 🔐 Admin Dashboard  
<img width="1365" height="611" alt="image" src="https://github.com/user-attachments/assets/c962f5af-d99d-4bd2-9e8d-22bb98ff7728" />

<img width="1350" height="617" alt="image" src="https://github.com/user-attachments/assets/32b3aa05-2fd7-4625-9bb3-b363c477a94f" />

---

## ⚙️ Installation & Setup

### **1. Clone or Download**
```bash
git clone https://github.com/yourusername/flask-blog-system.git
cd flask-blog-system
```

Or **download directly** 👇  
[![Download ZIP](https://img.shields.io/badge/⬇️%20Download%20ZIP-blue?style=for-the-badge)](https://example.com/your-flask-blog.zip)

---

### **2. Install Requirements**
```bash
pip install flask flask_sqlalchemy flask_login flask_wtf
```

---

### **3. Run the App**
```bash
python app.py
```
Then open in your browser:  
**http://127.0.0.1:5000**

---

## 🔑 Default Admin Login

```
Username: admin
Password: admin123
```

---

## 🗂 Project Structure

```
flask_blog_system/
│
├── app.py                # Main Flask app
├── models.py             # Database models
├── requirements.txt      # All dependencies
│
├── /templates            # HTML Templates
│   ├── base.html
│   ├── index.html
│   ├── post.html
│   ├── admin_dashboard.html
│   ├── login.html
│   ├── create_post.html
│
└── /static
    ├── style.css
```

---

## ✨ Upcoming Features
- ✅ Edit Post Functionality  
- ✅ Image Upload in CKEditor  
- ✅ Multiple Admins Support  

---

## 🤝 Contributing
Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to change.

---

## 📜 License
MIT License – Feel free to use and modify.
