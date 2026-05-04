from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai
from model import train_models, predict
from scoring import compute_score, classify_score
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import json
import re

# Load environment variables
load_dotenv()
if os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)

# Load ML models
models, vectorizer, results = train_models()

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        regNo TEXT,
        result TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER,
        type TEXT,
        data TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (account_id) REFERENCES accounts (id)
    )''')
    conn.commit()
    conn.close()

init_db()

# ---------------- API ----------------
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    hashed_password = generate_password_hash(password)
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO accounts (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        account_id = c.lastrowid
        conn.close()
        return jsonify({'message': 'Registered successfully', 'account_id': account_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id, password FROM accounts WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    
    if user and check_password_hash(user[1], password):
        return jsonify({'message': 'Login successful', 'account_id': user[0], 'username': username}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/history', methods=['POST'])
def save_history():
    data = request.json
    account_id = data.get('account_id')
    hist_type = data.get('type')
    hist_data = data.get('data') # Should be a JSON string or dict
    
    if isinstance(hist_data, dict):
        hist_data = json.dumps(hist_data)
        
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (account_id, type, data) VALUES (?, ?, ?)", 
              (account_id, hist_type, hist_data))
    conn.commit()
    conn.close()
    return jsonify({'message': 'History saved'}), 201

@app.route('/api/history/<int:account_id>', methods=['GET'])
def get_history(account_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id, type, data, timestamp FROM history WHERE account_id = ? ORDER BY timestamp DESC", (account_id,))
    rows = c.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            'id': row[0],
            'type': row[1],
            'data': json.loads(row[2]) if row[2] else {},
            'timestamp': row[3]
        })
    return jsonify({'history': history}), 200

@app.route('/api/history/<int:account_id>', methods=['DELETE'])
def clear_history(account_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM history WHERE account_id = ?", (account_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'History cleared'}), 200

@app.route('/predict', methods=['POST'])
def predict_api():
    data = request.json

    text = data.get('text', '')

    result = predict(text, models, vectorizer)

    # Compute scoring and classification
    score = compute_score(text)
    classification = classify_score(score)
    
    # Simple fallback sentiment analysis since we cannot install textblob
    positive_words = ['good', 'great', 'happy', 'better', 'well', 'fantastic', 'awesome', 'joy', 'excited']
    negative_words = ['bad', 'sad', 'depress', 'hopeless', 'empty', 'worthless', 'crying', 'numb', 'miserable', 'unhappy', 'low', 'anxious', 'stress', 'fear', 'scared', 'panic']
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if re.search(r'\b' + re.escape(word) + r'\b', text_lower))
    neg_count = sum(1 for word in negative_words if re.search(r'\b' + re.escape(word) + r'\b', text_lower))
    
    sentiment = 0.0
    if pos_count > neg_count:
        sentiment = 0.5
    elif neg_count > pos_count:
        sentiment = -0.5
        
    result.update({
        "score": score,
        "classification": classification,
        "sentiment": sentiment
    })


    # Save to DB
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, regNo, result) VALUES (?, ?, ?)",
              (data.get('name'), data.get('regNo'), str(result)))
    conn.commit()
    conn.close()
    # Add dataset metadata
    result["metadata"] = results
    return jsonify(result)



import csv
from io import StringIO
from flask import Response

@app.route('/download/users', methods=['GET'])
def download_users_csv():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id, name, regNo, result FROM users")
    users = c.fetchall()
    conn.close()

    # Generate CSV in memory
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Name', 'Reg No', 'Result'])
    cw.writerows(users)

    return Response(
        si.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=users_report.csv"}
    )

import random

# ── Intelligent Offline Chatbot Responses ──
OFFLINE_RESPONSES = {
    "greeting": [
        "Hello! 😊 I'm your Mind Matrix AI assistant. How are you feeling today? I'm here to listen and support you.",
        "Hi there! Welcome to Mind Matrix. I'm here to help you explore your mental wellbeing. What's on your mind?",
        "Hey! 👋 I'm glad you reached out. How can I support you today?",
    ],
    "anxiety": [
        "I understand that anxiety can feel overwhelming. Here are some things that might help right now:\n\n**🫁 Try the 4-7-8 breathing technique:**\n• Breathe in for 4 seconds\n• Hold for 7 seconds\n• Exhale slowly for 8 seconds\n• Repeat 3-4 times\n\nThis activates your parasympathetic nervous system and can reduce anxiety within minutes. You're not alone in this. 💚",
        "Anxiety is your body's natural response to stress, and it's more common than you think. **Here's a grounding exercise:**\n\nName **5 things you see**, **4 you can touch**, **3 you hear**, **2 you smell**, and **1 you taste**.\n\nThis brings your mind back to the present moment. Would you like to talk more about what's making you anxious?",
        "I hear you, and I want you to know that feeling anxious doesn't mean something is wrong with you. It means you care deeply.\n\n**Try this:** Place one hand on your chest and one on your belly. Take slow, deep breaths and focus on the hand rising on your belly. This simple act can calm your nervous system. 🌿",
    ],
    "depression": [
        "I'm really glad you're talking about this. Depression can make everything feel heavy, but reaching out is a brave and important step.\n\n**Small things that can help today:**\n• Step outside for even 5 minutes of sunlight ☀️\n• Drink a glass of water\n• Text or call someone you trust\n• Do one small thing that used to bring you joy\n\nYou don't have to do everything at once. One step at a time. 💙",
        "Thank you for sharing that with me. Depression often tells us we're alone, but that's not true.\n\n**Remember:** Your feelings are valid, but they are not permanent. Many people recover and find happiness again.\n\n**If you're in crisis**, please reach out to iCall: **9152987821** or AASRA: **9820466726**. You matter. 💚",
        "I understand how difficult this must be. Depression can drain your energy and make even simple tasks feel impossible.\n\n**Here's what I'd suggest:**\n• Be gentle with yourself today\n• Try to maintain a regular sleep schedule\n• Even a short 10-minute walk can boost your mood\n• Write down 3 things you're grateful for, no matter how small\n\nYou've already shown strength by reaching out. I'm here for you. 🌟",
    ],
    "stress": [
        "Stress is something most students and professionals deal with, so you're definitely not alone.\n\n**Try the Pomodoro Technique:**\n• Work for 25 minutes\n• Take a 5-minute break\n• After 4 cycles, take a 15-30 minute break\n\nThis prevents burnout and keeps your mind sharp. Also, remember: it's okay to say no to things that overwhelm you. 🧠",
        "Academic and work pressure can feel crushing, but there are ways to manage it.\n\n**Quick stress relief:**\n• Progressive muscle relaxation: Tense and release each muscle group from toes to head\n• Write a to-do list and prioritize just the top 3 tasks\n• Take a break from screens for 15 minutes\n\nWhat's causing you the most stress right now? Let's break it down together. 💪",
    ],
    "sleep": [
        "Sleep is incredibly important for mental health. Here are some evidence-based tips:\n\n**🌙 Sleep Hygiene Checklist:**\n• Set a consistent bedtime (even on weekends)\n• No screens 30 minutes before bed\n• Keep your room cool and dark\n• Avoid caffeine after 2 PM\n• Try a 10-minute guided meditation before sleep\n\nPoor sleep and mental health create a cycle — improving one helps the other. How long has sleep been an issue for you?",
    ],
    "lonely": [
        "Feeling lonely is painful, and I want you to know it's okay to feel this way. Many people experience loneliness, especially students in new environments.\n\n**Steps to reconnect:**\n• Reach out to one person today — even a simple \"Hey, how are you?\" text\n• Join a club, group, or online community around something you enjoy\n• Try volunteering — helping others can create meaningful connections\n\nYou deserve connection, and it starts with small steps. I'm here to talk anytime. 💛",
    ],
    "good": [
        "That's wonderful to hear! 😊 It's important to acknowledge the good days too.\n\n**To maintain your wellbeing:**\n• Keep up the habits that are working for you\n• Practice gratitude — write down what made today good\n• Share your positive energy with someone who might need it\n\nIs there anything specific you'd like to talk about or explore?",
        "I'm so happy to hear that! 🎉 Positive mental health is something to celebrate.\n\nRemember, wellness is a journey, not a destination. Keep nurturing the habits that make you feel good. What's been going well for you lately?",
    ],
    "thanks": [
        "You're very welcome! 😊 Remember, I'm always here whenever you need to talk. Take care of yourself — you deserve it! 💚",
        "Anytime! Taking the step to check in with yourself shows real self-awareness. Don't hesitate to come back whenever you need support. 🌟",
    ],
    "help": [
        "I'm here to help! Here's what I can assist you with:\n\n• **Mental health support** — Talk about anxiety, stress, depression, or any feelings\n• **Coping strategies** — Breathing exercises, grounding techniques, and more\n• **Wellness tips** — Sleep, exercise, and lifestyle guidance\n• **Crisis resources** — Emergency helpline numbers\n\nWhat would you like to explore? 💚",
    ],
    "default": [
        "Thank you for sharing that with me. I want you to know that your feelings are completely valid.\n\nCould you tell me a bit more about what you're experiencing? I'm here to listen without judgment and offer support where I can. 💚",
        "I appreciate you opening up. Mental health is a journey, and every conversation is a step forward.\n\nWould you like to talk about how you've been feeling lately, or would you prefer some wellness tips and coping strategies? I'm here for whatever you need. 🌿",
        "I hear you, and I'm glad you're reaching out. Sometimes just talking about things can make a big difference.\n\nIs there something specific on your mind today, or would you like me to share some relaxation techniques that might help? 😊",
    ],
}

def _get_offline_response(user_msg):
    """Intelligent keyword-based response selection for offline mode."""
    msg = user_msg.lower().strip()
    
    # Greeting patterns
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good evening', 'howdy', 'hii', 'hiii', 'sup', 'yo', 'greetings']
    if any(g in msg for g in greetings):
        return random.choice(OFFLINE_RESPONSES["greeting"])
    
    # Anxiety
    anxiety_words = ['anxious', 'anxiety', 'worried', 'worry', 'panic', 'nervous', 'fear', 'scared', 'overthink', 'racing heart', 'restless']
    if any(w in msg for w in anxiety_words):
        return random.choice(OFFLINE_RESPONSES["anxiety"])
    
    # Depression
    depression_words = ['depress', 'sad', 'hopeless', 'empty', 'worthless', 'crying', 'cry', 'give up', 'no point', 'lost interest', 'numb', 'miserable', 'unhappy', 'low mood', 'feeling down']
    if any(w in msg for w in depression_words):
        return random.choice(OFFLINE_RESPONSES["depression"])
    
    # Stress
    stress_words = ['stress', 'overwhelm', 'pressure', 'burnout', 'exhausted', 'too much', 'cant cope', 'overload', 'exam', 'deadline', 'assignment']
    if any(w in msg for w in stress_words):
        return random.choice(OFFLINE_RESPONSES["stress"])
    
    # Sleep
    sleep_words = ['sleep', 'insomnia', 'cant sleep', 'tired', 'fatigue', 'exhausted', 'nightmares', 'restless night']
    if any(w in msg for w in sleep_words):
        return random.choice(OFFLINE_RESPONSES["sleep"])
    
    # Loneliness
    lonely_words = ['lonely', 'alone', 'isolated', 'no friends', 'nobody', 'left out', 'disconnected']
    if any(w in msg for w in lonely_words):
        return random.choice(OFFLINE_RESPONSES["lonely"])
    
    # Positive
    good_words = ['good', 'great', 'happy', 'fine', 'amazing', 'wonderful', 'better', 'well', 'fantastic', 'awesome']
    if any(w in msg for w in good_words):
        return random.choice(OFFLINE_RESPONSES["good"])
    
    # Thanks
    thanks_words = ['thank', 'thanks', 'appreciate', 'helpful']
    if any(w in msg for w in thanks_words):
        return random.choice(OFFLINE_RESPONSES["thanks"])
    
    # Help
    help_words = ['help', 'what can you do', 'how does this work', 'features']
    if any(w in msg for w in help_words):
        return random.choice(OFFLINE_RESPONSES["help"])
    
    return random.choice(OFFLINE_RESPONSES["default"])

@app.route('/chat', methods=['POST'])
def chat_api():
    data = request.json
    messages = data.get('messages', [])
    last_msg = messages[-1]['content'] if messages else "Hello"
    
    # Try getting key from frontend, fallback to .env
    api_key = data.get('apiKey') or os.getenv("GEMINI_API_KEY")
    
    # If no valid API key, use offline mode
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        return jsonify({"response": _get_offline_response(last_msg)})

    try:
        # Reconfigure genai with the user's provided key from the frontend
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Format history for Gemini
        formatted_history = []
        for msg in messages[:-1]:
            role = "user" if msg['role'] == "user" else "model"
            formatted_history.append({"role": role, "parts": [msg['content']]})
            
        chat = model.start_chat(history=formatted_history)
        
        # Reinforce AI assistant persona
        prompt = f"You are an empathetic, professional AI mental health assistant. Be supportive, safe, and concise. Respond directly to the user's message: {last_msg}"
        
        response = chat.send_message(prompt)
        
        return jsonify({"response": response.text})
    except Exception as e:
        import traceback
        traceback.print_exc()
        # On ANY error (quota, network, etc.), fall back to offline mode
        return jsonify({"response": _get_offline_response(last_msg)})

if __name__ == '__main__':
    app.run(debug=True)
