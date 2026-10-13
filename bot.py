import os
import time
from playwright.sync_api import sync_playwright

URL_PAGE = "https://www.wiki-masters.com/login"
BOUTON_A_CLIQUER = "text=Nom du bouton"

NB_CLICS = 5
PAUSE_ENTRE_CLICS = 2

os.makedirs("captures", exist_ok=True)

with sync_playwright() as p:
    navigateur = p.chromium.launch(headless=True)
    contexte = navigateur.new_context(storage_state="session.json")
    page = contexte.new_page()
    page.goto(URL_PAGE)
    page.wait_for_timeout(3000)
    page.screenshot(path="captures/1_page.png", full_page=True)
    try:
        for i in range(NB_CLICS):
            page.click(BOUTON_A_CLIQUER, timeout=15000)
            time.sleep(PAUSE_ENTRE_CLICS)
            page.screenshot(path=f"captures/clic_{i + 1}.png")
    except Exception:
        page.screenshot(path="captures/erreur.png", full_page=True)
        raise
    navigateur.close()

print("ok")
