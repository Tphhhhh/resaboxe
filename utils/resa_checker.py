import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class ResaChecker:
    def __init__(self, resa_email, resa_password, telegram_notify=None):
        self.resa_email = resa_email
        self.resa_password = resa_password
        self.telegram_notify = telegram_notify

    def notify(self, message):
        if self.telegram_notify:
            try:
                self.telegram_notify(message)
                print("[✅] Notif Telegram envoyée.")
            except Exception as e:
                print(f"[❌] Erreur Telegram : {e}")
        else:
            print("[⚠️] Aucune fonction Telegram définie.")

    def run(self, day, hour, course_name, coach):
        print("[🔍] Démarrage de la surveillance...")

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        try:
            driver.get("https://www.resamania.com/connexion")
            driver.find_element(By.ID, "username").send_keys(self.resa_email)
            driver.find_element(By.ID, "password").send_keys(self.resa_password)
            driver.find_element(By.ID, "login-button").click()

            time.sleep(5)
            driver.get("https://www.resamania.com/mon-planning")
            time.sleep(5)

            cours = driver.find_elements(By.CLASS_NAME, "course-item")
            for c in cours:
                infos = c.text
                if day in infos and hour in infos and course_name.lower() in infos.lower() and coach.lower() in infos.lower():
                    if "Complet" not in infos:
                        message = f"✅ Une place est dispo : {infos}"
                        self.notify(message)
                        break
            else:
                print("[⏳] Aucune place libre détectée.")
        except Exception as e:
            print(f"[❌] Erreur surveillance : {e}")
        finally:
            driver.quit()
