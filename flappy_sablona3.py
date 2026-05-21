import pygame
import random

pygame.init()
pygame.mixer.init()

# -------------------------------------------------------
# NASTAVENÍ HRY
# -------------------------------------------------------
SIRKA = 400
VYSKA = 600
FPS = 60

PTACEK_X = 80
PTACEK_POLOMER = 18
TIZEN = 0.5
SKOK = -10

PILIR_SIRKA = 60
PILIR_MEZERA = 160
PILIR_RYCHLOST = 3

BARVA_POZADI     = (113, 197, 207)
BARVA_PTACEK     = (255, 220, 50)
BARVA_PILIR      = (100, 200, 80)
BARVA_TEXT       = (255, 255, 255)
BARVA_TLACITKO   = (50,  120, 200)
BARVA_TLACITKO_H = (80,  160, 255)   # barva při najetí myší (hover)
BARVA_ZAPNUTO    = (60,  200, 100)
BARVA_VYPNUTO    = (200,  80,  80)

# -------------------------------------------------------
# INICIALIZACE OKNA
# -------------------------------------------------------
okno = pygame.display.set_mode((SIRKA, VYSKA))
pygame.display.set_caption("Flappy Bird")
hodiny     = pygame.time.Clock()
font_velky = pygame.font.SysFont("Arial", 52, bold=True)
font_maly  = pygame.font.SysFont("Arial", 28)
font_tlac  = pygame.font.SysFont("Arial", 30, bold=True)

# -------------------------------------------------------
# NAČTENÍ ASSETŮ (ze série 2 – beze změny)
# -------------------------------------------------------
try:
    img_pozadi = pygame.transform.scale(
        pygame.image.load("obrazky/pozadi.png").convert_alpha(), (SIRKA, VYSKA))
    img_ptacek = pygame.transform.scale(
        pygame.image.load("obrazky/ptacek.png").convert_alpha(), (36, 36))
    img_pilir  = pygame.transform.scale(
        pygame.image.load("obrazky/pilir.png").convert_alpha(), (PILIR_SIRKA, VYSKA))
except Exception:
    img_pozadi = img_ptacek = img_pilir = None

try:
    zvuk_skok = pygame.mixer.Sound("zvuky/skok.wav");  zvuk_skok.set_volume(0.5)
    zvuk_bod  = pygame.mixer.Sound("zvuky/bod.wav");   zvuk_bod.set_volume(0.7)
    zvuk_smrt = pygame.mixer.Sound("zvuky/smrt.wav");  zvuk_smrt.set_volume(0.8)
except Exception:
    zvuk_skok = zvuk_bod = zvuk_smrt = None

# -------------------------------------------------------
# GLOBÁLNÍ STAV ZVUKU
# -------------------------------------------------------
zvuky_zapnuty = True    # True = zvuky hrají, False = ticho

# -------------------------------------------------------
# POMOCNÉ FUNKCE – KRESLENÍ (NEUPRAVUJTE)
# -------------------------------------------------------

def nakresli_pozadi(povrch):
    if img_pozadi:
        povrch.blit(img_pozadi, (0, 0))
    else:
        povrch.fill(BARVA_POZADI)

def nakresli_ptacka(povrch, y):
    if img_ptacek:
        povrch.blit(img_ptacek, (PTACEK_X - 18, int(y) - 18))
    else:
        pygame.draw.circle(povrch, BARVA_PTACEK, (PTACEK_X, int(y)), PTACEK_POLOMER)
        pygame.draw.circle(povrch, (200, 160, 0), (PTACEK_X, int(y)), PTACEK_POLOMER, 3)

def nakresli_pilire(povrch, pilire):
    for pilir in pilire:
        horni_vyska   = pilir["mezera_y"] - PILIR_MEZERA // 2
        dolni_zacatek = pilir["mezera_y"] + PILIR_MEZERA // 2
        if img_pilir:
            h = pygame.transform.scale(pygame.transform.flip(img_pilir, False, True),
                                       (PILIR_SIRKA, horni_vyska))
            povrch.blit(h, (pilir["x"], 0))
            d = pygame.transform.scale(img_pilir, (PILIR_SIRKA, VYSKA - dolni_zacatek))
            povrch.blit(d, (pilir["x"], dolni_zacatek))
        else:
            pygame.draw.rect(povrch, BARVA_PILIR, (pilir["x"], 0, PILIR_SIRKA, horni_vyska))
            pygame.draw.rect(povrch, BARVA_PILIR, (pilir["x"], dolni_zacatek,
                                                    PILIR_SIRKA, VYSKA - dolni_zacatek))

def nakresli_skore(povrch, skore):
    text = font_velky.render(str(skore), True, BARVA_TEXT)
    povrch.blit(text, (SIRKA // 2 - text.get_width() // 2, 30))

def obrazovka_konec(povrch, skore):
    prekryv = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
    prekryv.fill((0, 0, 0, 140))
    povrch.blit(prekryv, (0, 0))
    for text, y, barva in [
        (font_velky.render("Konec hry!", True, (255, 80, 80)),   200, None),
        (font_maly.render(f"Skóre: {skore}", True, BARVA_TEXT), 280, None),
        (font_maly.render("Mezerník = menu",  True, BARVA_TEXT), 330, None),
    ]:
        povrch.blit(text, (SIRKA // 2 - text.get_width() // 2, y))

def zahraj(zvuk):
    if zvuky_zapnuty and zvuk:
        zvuk.play()

def vytvor_pilir():
    return {"x": SIRKA, "mezera_y": random.randint(150, VYSKA - 150)}

# -------------------------------------------------------
# POMOCNÁ FUNKCE – TLAČÍTKO (NEUPRAVUJTE)
# -------------------------------------------------------

def nakresli_tlacitko(povrch, text, rect, barva):
    """
    Nakreslí obdélníkové tlačítko se zaoblením a popiskem.
    rect = (x, y, sirka, vyska)
    Vrátí True, pokud je na tlačítku myš (hover).
    """
    mys_x, mys_y = pygame.mouse.get_pos()
    hover = pygame.Rect(rect).collidepoint(mys_x, mys_y)
    barva_pouzita = BARVA_TLACITKO_H if hover else barva
    pygame.draw.rect(povrch, barva_pouzita, rect, border_radius=12)
    pygame.draw.rect(povrch, BARVA_TEXT, rect, 2, border_radius=12)
    napis = font_tlac.render(text, True, BARVA_TEXT)
    povrch.blit(napis, (rect[0] + rect[2] // 2 - napis.get_width() // 2,
                        rect[1] + rect[3] // 2 - napis.get_height() // 2))
    return hover

# -------------------------------------------------------
# DEFINICE TLAČÍTEK
#
#  Každé tlačítko je slovník s klíči:
#    "text"  – nápis na tlačítku
#    "rect"  – (x, y, šířka, výška)
#    "akce"  – řetězec, který identifikuje co tlačítko dělá
#
#  Akce:
#    "hrat"   – spustí hru
#    "zvuk"   – přepne zvuk zap/vyp
#    "konec"  – ukončí program
# -------------------------------------------------------

TLACITKA = [
    {"text": "Hrát",         "rect": (100, 220, 200, 55), "akce": "hrat"},
    {"text": "Zvuk: ZAP",    "rect": (100, 300, 200, 55), "akce": "zvuk"},
    {"text": "Konec",        "rect": (100, 380, 200, 55), "akce": "konec"},
]

# ============================================================
#  BLOK A – VYKRESLENÍ MENU  ← VÁŠ ÚKOL
#
#  Napište funkci nakresli_menu(povrch), která:
#
#  1) Vyplní pozadí barvou BARVA_POZADI (nebo nakreslí img_pozadi)
#
#  2) Vykreslí nadpis "Flappy Bird" uprostřed nahoře (y ≈ 100)
#     pomocí font_velky.render(...) a povrch.blit(...)
#
#  3) Pro každé tlačítko v seznamu TLACITKA zavolá nakresli_tlacitko()
#     Pozor: tlačítko "zvuk" musí měnit barvu a text podle toho,
#     zda jsou zvuky zapnuté:
#       - zvuky_zapnuty == True  → text "Zvuk: ZAP",  barva BARVA_ZAPNUTO
#       - zvuky_zapnuty == False → text "Zvuk: VYP",  barva BARVA_VYPNUTO
#     Pro ostatní tlačítka použij BARVA_TLACITKO.
#
#  NÁPOVĚDA – jak vykreslit text uprostřed:
#    napis = font_velky.render("Hello", True, BARVA_TEXT)
#    povrch.blit(napis, (SIRKA // 2 - napis.get_width() // 2, 100))
#
#  NÁPOVĚDA – jak projet seznam tlačítek:
#    for tlacitko in TLACITKA:
#        nakresli_tlacitko(povrch, tlacitko["text"], tlacitko["rect"], barva)
# ============================================================

def nakresli_menu(povrch):
    if img_pozadi:
        povrch.blit(img_pozadi, (0, 0))
    else:
        povrch.fill(BARVA_POZADI)

    napis = font_velky.render("Flappy Brno", True, BARVA_TEXT)
    povrch.blit(napis, (SIRKA // 2 - napis.get_width() // 2, 100))

    for tlacitko in TLACITKA:
        nakresli_tlacitko(povrch, tlacitko["text"], tlacitko["rect"], BARVA_TLACITKO)


    pass   # ← toto smažte a napište svůj kód


# ============================================================
#  BLOK B – SMYČKA MENU  ← VÁŠ ÚKOL
#
#  Napište funkci menu(), která zobrazí menu a čeká na kliknutí.
#
#  Struktura funkce:
#
#  def menu():
#      global zvuky_zapnuty
#      while True:
#          hodiny.tick(FPS)
#
#          # 1) Projděte události (pygame.event.get())
#          #    - QUIT → pygame.quit() a return
#          #    - MOUSEBUTTONDOWN (udalost.type == pygame.MOUSEBUTTONDOWN)
#          #      Pro každé tlačítko zkontrolujte, zda bylo kliknuto:
#          #        pygame.Rect(tlacitko["rect"]).collidepoint(udalost.pos)
#          #      Podle akce (tlacitko["akce"]):
#          #        "hrat"  → zavolejte hra() a po návratu pokračujte
#          #        "zvuk"  → přepněte: zvuky_zapnuty = not zvuky_zapnuty
#          #        "konec" → pygame.quit() a return
#
#          # 2) Zavolejte nakresli_menu(okno)
#
#          # 3) pygame.display.flip()
#
#  NÁPOVĚDA – detekce kliknutí na tlačítko:
#    if pygame.Rect(tlacitko["rect"]).collidepoint(udalost.pos):
#        ...
# ============================================================

# --- Sem napište funkci menu() ---

def menu():
    global zvuky_zapnuty
    while True:
        hodiny.tick(FPS)
        
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                return
            if udalost.type == pygame.MOUSEBUTTONDOWN:
                for tlacitko in TLACITKA:
                    if pygame.Rect(tlacitko["rect"]).collidepoint(udalost.pos):
                        hra()

          # 1) Projděte události (pygame.event.get())
          #    - QUIT → pygame.quit() a return -----------DONE
          #    - MOUSEBUTTONDOWN (udalost.type == pygame.MOUSEBUTTONDOWN) ----DONE
          #      Pro každé tlačítko zkontrolujte, zda bylo kliknuto:
          #        pygame.Rect(tlacitko["rect"]).collidepoint(udalost.pos)
          #      Podle akce (tlacitko["akce"]):
          #        "hrat"  → zavolejte hra() a po návratu pokračujte
          #        "zvuk"  → přepněte: zvuky_zapnuty = not zvuky_zapnuty
          #        "konec" → pygame.quit() a return

          # 2) Zavolejte nakresli_menu(okno)

    pygame.display.flip()
# -------------------------------------------------------
# HERNÍ SMYČKA (hotová, pouze opravené skóre)
# -------------------------------------------------------

def hra():
    global zvuky_zapnuty
    ptacek_y  = VYSKA // 2
    ptacek_vy = 0
    skore     = 0
    bezi      = True
    pilire    = [vytvor_pilir()]

    while True:
        hodiny.tick(FPS)

        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                return
            if udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_SPACE:
                    if bezi:
                        ptacek_vy = SKOK
                        zahraj(zvuk_skok)
                    else:
                        return   # zpět do menu

        if bezi:
            ptacek_vy += TIZEN
            ptacek_y  += ptacek_vy
            if ptacek_y - PTACEK_POLOMER < 0 or ptacek_y + PTACEK_POLOMER > VYSKA:
                bezi = False
                zahraj(zvuk_smrt)

        if bezi:
            for pilir in pilire:
                pilir["x"] -= PILIR_RYCHLOST
            pilire = [p for p in pilire if p["x"] > -PILIR_SIRKA]
            if pilire[-1]["x"] < SIRKA - 200:
                pilire.append(vytvor_pilir())

        if bezi:
            for pilir in pilire:
                prekryv_x   = (PTACEK_X + PTACEK_POLOMER > pilir["x"] and
                               PTACEK_X - PTACEK_POLOMER < pilir["x"] + PILIR_SIRKA)
                mimo_mezeru = (ptacek_y - PTACEK_POLOMER < pilir["mezera_y"] - PILIR_MEZERA // 2 or
                               ptacek_y + PTACEK_POLOMER > pilir["mezera_y"] + PILIR_MEZERA // 2)
                if prekryv_x and mimo_mezeru:
                    bezi = False
                    zahraj(zvuk_smrt)
                if pilir["x"] + PILIR_SIRKA < PTACEK_X and not pilir.get("zapocitan", False):
                    skore += 1
                    pilir["zapocitan"] = True
                    zahraj(zvuk_bod)

        nakresli_pozadi(okno)
        nakresli_pilire(okno, pilire)
        nakresli_ptacka(okno, ptacek_y)
        nakresli_skore(okno, skore)

        if not bezi:
            obrazovka_konec(okno, skore)

        pygame.display.flip()

# -------------------------------------------------------
# SPUŠTĚNÍ
# -------------------------------------------------------
menu()

pygame.quit()
