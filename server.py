import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = "gemini-2.5-flash"
API_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"models/{MODEL}:generateContent"
)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "name": "Mimi AI",
        "status": "running",
        "message": "مرحبا، ميمي جاهزة"
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "اكتب رسالتك أولا"}), 400

    if not API_KEY:
        return jsonify({
            "error": "مفتاح الذكاء الاصطناعي غير مضاف للخادم"
        }), 503

    try:
        response = requests.post(
            API_URL,
            params={"key": API_KEY},
            json={
                "contents": [{
                    "parts": [{"text": message}]
                }]
            },
            timeout=60
        )

        if response.status_code != 200:
            return jsonify({
                "error": "تعذر الاتصال بخدمة الذكاء الاصطناعي",
                "details": response.text[:500]
            }), 502

        result = response.json()
        reply = result["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({"reply": reply})

    except Exception:
        return jsonify({
            "error": "حدث خطأ أثناء الاتصال، حاول مرة أخرى"
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
