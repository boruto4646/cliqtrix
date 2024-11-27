from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Wikipedia API URL
WIKIPEDIA_API_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"
# LibreTranslate API URL
LIBRETRANSLATE_API_URL = "https://libretranslate.com/translate"

@app.route('/zobot-webhook', methods=['POST'])
def zobot_webhook():
    data = request.json
    query = data.get("query", "")
    user_language = data.get("language", "en")

    # Translate query to English (if needed)
    if user_language != "en":
        translate_response = requests.post(LIBRETRANSLATE_API_URL, json={
            "q": query,
            "source": user_language,
            "target": "en"
        })
        query = translate_response.json().get("translatedText", query)

    # Fetch information from Wikipedia
    wiki_response = requests.get(WIKIPEDIA_API_URL + query)
    wiki_summary = wiki_response.json().get("extract", "No information found.")

    # Translate response back to user's language (if needed)
    if user_language != "en":
        reverse_translate_response = requests.post(LIBRETRANSLATE_API_URL, json={
            "q": wiki_summary,
            "source": "en",
            "target": user_language
        })
        wiki_summary = reverse_translate_response.json().get("translatedText", wiki_summary)

    # Respond back to Zobot
    return jsonify({"response": wiki_summary})

if __name__ == "__main__":
    app.run(port=5000)
