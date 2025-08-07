import os
import smtplib
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from email.message import EmailMessage

# Load environment variables
load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-email', methods=['POST'])
def generate_email():
    prompt = request.json.get('prompt', '')

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",  # ✅ Updated model
        "messages": [
            {"role": "user", "content": f"Write a professional email for: {prompt}"}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    print("Groq API status:", response.status_code)
    print("Groq API response:", response.text)

    try:
        result = response.json()
        ai_email = result['choices'][0]['message']['content']
        return jsonify({"email": ai_email})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to generate email. Check your model name or API key."}), 500

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    to_email = data['to']
    subject = data['subject']
    body = data['body']

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = to_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)

        return jsonify({"success": True})
    except Exception as e:
        print("Error sending email:", e)
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
