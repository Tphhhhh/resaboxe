from flask import Flask, render_template, request
import threading
import os
from utils.resa_checker import ResaChecker

app = Flask(__name__)
bot_thread = None

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
            day=day,
            hour=hour,
            course_name=course_name,
            coach=coach
        )

        bot_thread = threading.Thread(target=bot.run)
        bot_thread.start()

        return "Surveillance lancée avec succès !"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
