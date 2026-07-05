from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Create the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Temporary chat memory (clears when the server restarts)
chat_history = [
    {
        "role": "system",
        "content": (
            "You are JARVIS, an intelligent AI assistant. "
            "You are calm, helpful, intelligent, and concise. "
            "Address the user politely and answer naturally."
        ),
    }
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"reply": "Please say something."})

    chat_history.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=chat_history,
            temperature=0.7,
        )

        assistant_reply = response.choices[0].message.content

        chat_history.append(
            {
                "role": "assistant",
                "content": assistant_reply,
            }
        )

        return jsonify({"reply": assistant_reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
