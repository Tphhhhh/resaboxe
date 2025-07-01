import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import smtplib
from email.mime.text import MIMEText

class ResaChecker:
    def __init__(self, resa_email, resa_password, email_target=None, telegram_notify=None):
        self.resa_email = resa_email
        self.resa_password = resa_password
        self.email_target = email_target
        self.telegram_notify = telegram_notify

    def send_email(self, subject, message):
        if not self.email_target:
            return
        try:
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = self.resa_email
            msg['To'] = self.email_target

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.resa_email, self.resa_password)
                smtp.send_message(msg)
            print("[✅] Email envoyé avec succès.")
        except Exception as e:
            print(f"[❌] Erreur lors de l'envoi de l'email : {e}")

    def notify(self, message):
        if self.telegram_notify:
            try:
                self.telegram_notify(message)
            except Exception as e:
                print(f"[❌] Erreur Telegram : {e}")
        self.send_email("💥 Place dispo !", message)

    def run(self, day, hour, course_name, coach):
        print("[🔍] Démarrage de la surveillance...")
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        try:
            driver.get("https://www.resamania.com/connexion")

            # Login
            driver.find_element(By.ID, "username").send_keys(self.resa_email)
            driver.find_element(By.ID, "password").send_keys(self.resa_password)
            driver.find_element(By.ID, "login-button").click()

            time.sleep(5)

            # Aller à la page des cours
            driver.get("https://www.resamania.com/mon-planning")
            time.sleep(5)

            # Extrait les infos (adapté selon ton HTML réel)
            cours = driver.find_elements(By.CLASS_NAME, "course-item")
            for c in cours:
                infos = c.text
                if day in infos and hour in infos and course_name.lower() in infos.lower() and coach.lower() in infos.lower():
                    if "Complet" not in infos:
                        message = f"✅ Une place est dispo : {infos}"
                        self.notify(message)
                        break
            else:
                print("[⏳] Aucune place libre détectée pour le moment.")

        except Exception as e:
            print(f"[❌] Erreur dans la surveillance : {e}")
        finally:
            driver.quit()
