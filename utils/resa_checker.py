from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
import os

class ResaChecker:
    def __init__(self, day, hour, course_name, coach):
        self.day = day.lower()
        self.hour = hour
        self.course_name = course_name.lower()
        self.coach = coach.lower()
        self.telegram_token = "8056511205:AAEb4f-ErcwqWcXplBZGCwAT-xZwxqNPON8"
        self.telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")  # à configurer juste après
        self.resa_email = os.environ.get("RESA_EMAIL")
        self.resa_password = os.environ.get("RESA_PASSWORD")

    def send_telegram(self, message):
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": message
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Notification Telegram envoyée")
        else:
            print("❌ Échec Telegram :", response.text)

    def check_and_notify(self):
        print("🚀 Lancement de Selenium…")
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)

        try:
            driver.get("https://member.resamania.com/templenobleart/planning?club=%2Ftemplenobleart%2Fclubs%2F646")

            # Connexion
            login_btn = driver.find_element(By.LINK_TEXT, "Connexion")
            login_btn.click()
            time.sleep(2)

            email_input = driver.find_element(By.NAME, "email")
            password_input = driver.find_element(By.NAME, "password")

            email_input.send_keys(self.resa_email)
            password_input.send_keys(self.resa_password)
            driver.find_element(By.TAG_NAME, "button").click()
            time.sleep(5)

            page_source = driver.page_source.lower()
            if self.day in page_source and self.hour in page_source and self.course_name in page_source and self.coach in page_source:
                print("🎯 Le cours existe !")
                if "réserver" in page_source:
                    message = f"📢 Une place s’est libérée pour : {self.course_name} à {self.hour} avec {self.coach} !"
                    self.send_telegram(message)
                else:
                    print("ℹ️ Le cours est encore complet.")
            else:
                print("❌ Cours non trouvé.")

        except Exception as e:
            print(f"⚠️ Erreur : {e}")
        finally:
            driver.quit()
