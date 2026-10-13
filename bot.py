import os
from playwright.sync_api import sync_playwright

URL_PAGE = "https://www.wiki-masters.com/login"
NB_PAQUETS_MAX = 10
ATTENTE = 2500

os.makedirs("captures", exist_ok=True)

with sync_playwright() as p:
    navigateur = p.chromium.launch(headless=True)
    contexte = navigateur.new_context(storage_state="session.json")
    page = contexte.new_page()
    page.goto(URL_PAGE)
    page.wait_for_timeout(3000)
    page.screenshot(path="captures/0_page.png", full_page=True)

    ouvrir = page.locator("button:has(img[alt='Ouvrir un paquet'])").first
    fleche = page.locator("svg:has(polyline[points='9 18 15 12 9 6'])").first
    continuer = page.locator("button:has-text('Continuer')").first

    try:
        if ouvrir.count() == 0:
            raise Exception("bouton Ouvrir introuvable, la session a peut-etre expire")

        paquets_ouverts = 0
        for paquet in range(NB_PAQUETS_MAX):
            page.wait_for_timeout(ATTENTE)
            if not ouvrir.is_visible() or not ouvrir.is_enabled():
                break
            ouvrir.click()
            paquets_ouverts += 1

            for etape in range(60):
                page.wait_for_timeout(ATTENTE)
                try:
                    if continuer.is_visible():
                        continuer.click(timeout=5000)
                    elif fleche.is_visible():
                        fleche.click(timeout=5000)
                    elif ouvrir.is_visible():
                        break
                except Exception:
                    page.screenshot(path=f"captures/attente_{paquet + 1}_{etape}.png")
                    page.wait_for_timeout(5000)

            page.screenshot(path=f"captures/paquet_{paquet + 1}.png")
    except Exception:
        page.screenshot(path="captures/erreur.png", full_page=True)
        raise

    navigateur.close()

print("ok,", paquets_ouverts, "paquets ouverts")
