import time
import smtplib
from email.mime.text import MIMEText

class ResaChecker:
    def __init__(self, resa_email, resa_password, email_target, day, hour, course_name, coach):
        self.resa_email = resa_email
        self.resa_password = resa_password
        self.email_target = email_target
        self.day = day
        self.hour = hour
        self.course_name = course_name
        self.coach = coach

    def run(self):
        print("🔍 Surveillance lancée pour :", self.day, self.hour, self.course_name, self.coach)
        time.sleep(5)  # simulation

        # 💡 Simulation de dispo trouvée
        self.send_email()

    def send_email(self):
        msg = MIMEText(f"📢 Une place s'est libérée pour : {self.course_name} le {self.day} à {self.hour} avec {self.coach}")
        msg['Subject'] = "⚠️ Cours de boxe dispo !"
        msg['From'] = self.resa_email
        msg['To'] = self.email_target

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.resa_email, self.resa_password)
                smtp.send_message(msg)
            print("✅ Email envoyé à", self.email_target)
        except Exception as e:
            print("❌ Erreur envoi mail :", e)
