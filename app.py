from flask import Flask, render_template, request
import threading
import os
import requests
from utils.resa_checker import ResaChecker

app = Flask(__name__)
bot_thread = None

def send_telegram_message(message):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": message}
        try:
            requests.post(url, data=data)
        except Exception as e:
            print(f"[Erreur envoi Telegram] {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    global bot_thread

    if request.method == "POST":
        day = request.form.get("day")
        hour = request.form.get("hour")
        course_name = request.form.get("course_name")
        coach = request.form.get("coach")

        if bot_thread and bot_thread.is_alive():
            return "Bot déjà en cours de surveillance."

        bot = ResaChecker(
            resa_email=os.environ.get("RESA_EMAIL"),
            resa_password=os.environ.get("RESA_PASSWORD"),
            email_target=os.environ.get("EMAIL_TARGET"),
            telegram_notify=send_telegram_message  # ⬅️ Ajout de la fonction de notif
        )

        bot_thread = threading.Thread(target=bot.run, args=(day, hour, course_name, coach))
        bot_thread.start()

        return "Surveillance lancée avec succès !"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
