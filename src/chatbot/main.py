from flask import Flask, request, jsonify
import openai
import os
import sys
from dotenv import load_dotenv

# ✅ Fix: Ensure the script finds `src` folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from browser_automation.web_scraper import search_google  # ✅ Fix import

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Debugging - Check if API Key is loaded
if not OPENAI_API_KEY:
    raise ValueError("🚨 ERROR: OPENAI_API_KEY is missing! Add it to the .env file.")

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    """
    Flask API endpoint that processes chat messages.
    - If message starts with 'search:', perform a Google search.
    - Otherwise, interact with OpenAI API.
    """
    data = request.get_json()
    user_message = data.get('message')

    if user_message.lower().startswith("search:"):
        search_results = search_google(user_message.replace("search:", "").strip())
        return jsonify({'reply': search_results})
    
    # ✅ Fix OpenAI API call for version 1.0.0+
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": user_message}]
    )

    return jsonify({'reply': response.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
