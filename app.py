from flask import Flask, render_template, request, jsonify
from chatbot import StressBot
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Initialize chatbot
chatbot = StressBot()

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = chatbot.process_message(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True) 