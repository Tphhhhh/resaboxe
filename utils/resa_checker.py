import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
            # Connexion à l'interface Temple Noble Art
            driver.get("https://api.resamania.com/oauth/login/templenobleart?client_id=26_2532ba2d23446346e4f83dda1570fdd224ce70c546251c4ce84bd734e0e18811&redirect_uri=https://member.resamania.com/templenobleart/&response_type=code")

            # Attendre que le champ email soit visible
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login_step_login_username")))

            # Remplir email et mot de passe
            driver.find_element(By.ID, "login_step_login_username").send_keys(self.resa_email)
            driver.find_element(By.ID, "_password").send_keys(self.resa_password)

            # Cliquer sur le bouton de connexion
            driver.find_element(By.XPATH, "//button[contains(text(), 'Connexion')]").click()

            # Attendre la redirection
            time.sleep(5)
            driver.get("https://member.resamania.com/templenobleart/planning")
            time.sleep(5)

            # Analyse des cours disponibles
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
