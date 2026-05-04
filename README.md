# MindMatrix AI 🧠

MindMatrix is a comprehensive full-stack mental health diagnostic and support application. It leverages Machine Learning, Natural Language Processing (NLP), and Generative AI to analyze user text, predict mental health conditions, calculate stress levels, and provide empathetic conversational support.

## 🚀 Features

*   **Machine Learning Diagnostics:** Predicts the likelihood of mental health conditions using 5 different ML models (Naive Bayes variants, Logistic Regression, SVM) based on user text input using TF-IDF vectorization.
*   **Custom Symptom Scoring & Classification:** An NLP-based algorithm calculates symptom scores by assigning weights to stress, anxiety, and depression keywords. It classifies states as *Normal*, *Mild Stress*, or *High Stress*.
*   **Sentiment Analysis:** Analyzes the polarity of user input to detect positive or negative emotional states.
*   **AI Chatbot Assistant:** Features an empathetic chatbot powered by Google Gemini (gemini-2.0-flash). 
*   **Intelligent Offline Fallback:** If the API or network fails, the chatbot falls back to a robust keyword-matching system to ensure users always receive supportive responses.
*   **Report Generation:** Users can download their diagnostic results in a clean, professional format.
*   **Secure Authentication:** User accounts are protected with hashed passwords via Werkzeug.

## 🛠️ Technology Stack

*   **Frontend:** HTML5, Vanilla CSS, JavaScript
*   **Backend:** Python, Flask, Flask-CORS
*   **Database:** SQLite
*   **Machine Learning:** scikit-learn, pandas, numpy
*   **Generative AI:** google-generativeai (Gemini API)

## ⚙️ Installation & Setup

### Prerequisites
*   Python 3.8+
*   Node.js & npm (for serving the frontend)

### Backend Setup
1. Open a terminal and navigate to the `Backend` directory:
   ```bash
   cd Backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `Backend` directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```
5. Start the Flask server:
   ```bash
   python app.py
   ```
   *The backend will run on `http://127.0.0.1:5000`*

### Frontend Setup
1. Open a new terminal and navigate to the `Frontend` directory:
   ```bash
   cd Frontend
   ```
2. You can serve the frontend using any local web server. For example, using Python:
   ```bash
   python -m http.server 8080
   ```
3. Open your browser and go to `http://localhost:8080`.

## 📁 Project Structure

*   `Backend/` - Contains the Flask application, database files, and machine learning models.
    *   `app.py` - The main server entry point.
    *   `scoring.py` - Custom NLP scoring and classification logic.
    *   `model.py` - Machine learning model training and prediction logic.
*   `Frontend/` - Contains the HTML, CSS, and JS files for the user interface.
*   `Viva_Preparation_Guide.md` - A comprehensive guide detailing the internal logic, system flow, and potential viva questions.

## 🤝 Contribution
Feel free to fork the repository, make improvements, and create pull requests.
