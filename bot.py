import os
import time
from playwright.sync_api import sync_playwright

URL_LOGIN = "https://exemple.com/login"
URL_PAGE = "https://exemple.com/page-du-bouton"
IDENTIFIANT = os.environ["IDENTIFIANT"]
MOT_DE_PASSE = os.environ["MOT_DE_PASSE"]

CHAMP_IDENTIFIANT = "input[name='email']"
CHAMP_MOT_DE_PASSE = "input[name='password']"
BOUTON_CONNEXION = "button[type='submit']"
BOUTON_A_CLIQUER = "text=Nom du bouton"

NB_CLICS = 5
PAUSE_ENTRE_CLICS = 2

with sync_playwright() as p:
    navigateur = p.chromium.launch(headless=True)
    page = navigateur.new_page()
    page.goto(URL_LOGIN)
    page.fill(CHAMP_IDENTIFIANT, IDENTIFIANT)
    page.fill(CHAMP_MOT_DE_PASSE, MOT_DE_PASSE)
    page.click(BOUTON_CONNEXION)
    page.wait_for_load_state("networkidle")
    page.goto(URL_PAGE)
    for i in range(NB_CLICS):
        page.click(BOUTON_A_CLIQUER)
        time.sleep(PAUSE_ENTRE_CLICS)
    navigateur.close()

print("ok")
