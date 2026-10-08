import pygame
import random

pygame.init()
pygame.mixer.init()   # zapne zvukový systém

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

BARVA_POZADI  = (113, 197, 207)
BARVA_PTACEK  = (255, 220, 50)
BARVA_PILIR   = (100, 200, 80)
BARVA_TEXT    = (255, 255, 255)

# -------------------------------------------------------
# STRUKTURA SLOŽEK
#
#  flappy/
#  ├── flappy_sablona2.py    ← tento soubor
#  ├── obrazky/
#  │   ├── pozadi.png        (400 × 600 px)
#  │   ├── ptacek.png        (36 × 36 px, průhledné PNG)
#  │   └── pilir.png         (60 × 600 px, průhledné PNG)
#  └── zvuky/
#      ├── skok.wav
#      ├── bod.wav
#      └── smrt.wav
#
#  Soubory najdete na sdíleném disku kroužku.
#  Pokud obrázek nebo zvuk chybí, hra spadne – zkontrolujte cestu!
# -------------------------------------------------------

# ============================================================
#  BLOK A – NAČTENÍ OBRÁZKŮ  ← VÁŠ ÚKOL
#
#  Načtěte obrázky pomocí pygame.image.load() a .convert_alpha()
#  a uložte je do proměnných. Poté je upravte na správnou velikost
#  pomocí pygame.transform.scale().
#
#  Co načíst:
#    img_pozadi  – "obrazky/pozadi.png"   → velikost (SIRKA, VYSKA)
#    img_ptacek  – "obrazky/ptacek.png"   → velikost (36, 36)
#    img_pilir   – "obrazky/pilir.png"    → velikost (PILIR_SIRKA, VYSKA)
#
#  NÁPOVĚDA:
#    obrazek = pygame.image.load("cesta/soubor.png").convert_alpha()
#    obrazek = pygame.transform.scale(obrazek, (sirka, vyska))
# ============================================================

# --- Sem napište načítání obrázků ---


# ============================================================
#  BLOK B – NAČTENÍ ZVUKŮ  ← VÁŠ ÚKOL
#
#  Načtěte zvukové soubory pomocí pygame.mixer.Sound() a uložte
#  je do proměnných.
#
#  Co načíst:
#    zvuk_skok  – "zvuky/skok.wav"
#    zvuk_bod   – "zvuky/bod.wav"
#    zvuk_smrt  – "zvuky/smrt.wav"
#
#  NÁPOVĚDA:
#    zvuk = pygame.mixer.Sound("zvuky/soubor.wav")
#    zvuk.set_volume(0.5)   # hlasitost 0.0 až 1.0 (volitelné)
# ============================================================

# --- Sem napište načítání zvuků ---


# -------------------------------------------------------
# INICIALIZACE OKNA
# -------------------------------------------------------
okno = pygame.display.set_mode((SIRKA, VYSKA))
pygame.display.set_caption("Flappy Bird")
hodiny = pygame.time.Clock()
font_velky = pygame.font.SysFont("Arial", 52, bold=True)
font_maly  = pygame.font.SysFont("Arial", 28)

# -------------------------------------------------------
# POMOCNÉ FUNKCE – KRESLENÍ (NEUPRAVUJTE)
# -------------------------------------------------------

def nakresli_pozadi(povrch):
    """Nakreslí pozadí – obrázek nebo záložní barvu."""
    try:
        povrch.blit(img_pozadi, (0, 0))
    except NameError:
        povrch.fill(BARVA_POZADI)

def nakresli_ptacka(povrch, y):
    """Nakreslí ptáčka – sprite nebo záložní kroužek."""
    try:
        povrch.blit(img_ptacek, (PTACEK_X - 18, int(y) - 18))
    except NameError:
        pygame.draw.circle(povrch, BARVA_PTACEK, (PTACEK_X, int(y)), PTACEK_POLOMER)
        pygame.draw.circle(povrch, (200, 160, 0), (PTACEK_X, int(y)), PTACEK_POLOMER, 3)

def nakresli_pilire(povrch, pilire):
    """Nakreslí pilíře – sprite nebo záložní obdélníky."""
    for pilir in pilire:
        horni_vyska   = pilir["mezera_y"] - PILIR_MEZERA // 2
        dolni_zacatek = pilir["mezera_y"] + PILIR_MEZERA // 2
        try:
            # Horní pilíř – obrátíme svisle (flip)
            horni = pygame.transform.flip(img_pilir, False, True)
            horni = pygame.transform.scale(horni, (PILIR_SIRKA, horni_vyska))
            povrch.blit(horni, (pilir["x"], 0))
            # Dolní pilíř
            dolni = pygame.transform.scale(img_pilir, (PILIR_SIRKA, VYSKA - dolni_zacatek))
            povrch.blit(dolni, (pilir["x"], dolni_zacatek))
        except NameError:
            pygame.draw.rect(povrch, BARVA_PILIR,
                             (pilir["x"], 0, PILIR_SIRKA, horni_vyska))
            pygame.draw.rect(povrch, BARVA_PILIR,
                             (pilir["x"], dolni_zacatek, PILIR_SIRKA, VYSKA - dolni_zacatek))

def nakresli_skore(povrch, skore):
    text = font_velky.render(str(skore), True, BARVA_TEXT)
    povrch.blit(text, (SIRKA // 2 - text.get_width() // 2, 30))

def obrazovka_konec(povrch, skore):
    prekryv = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
    prekryv.fill((0, 0, 0, 140))
    povrch.blit(prekryv, (0, 0))
    t1 = font_velky.render("Konec hry!", True, (255, 80, 80))
    t2 = font_maly.render(f"Skóre: {skore}", True, BARVA_TEXT)
    t3 = font_maly.render("Mezerník = znovu hrát", True, BARVA_TEXT)
    povrch.blit(t1, (SIRKA//2 - t1.get_width()//2, 200))
    povrch.blit(t2, (SIRKA//2 - t2.get_width()//2, 280))
    povrch.blit(t3, (SIRKA//2 - t3.get_width()//2, 330))

def vytvor_pilir():
    mezera_y = random.randint(150, VYSKA - 150)
    return {"x": SIRKA, "mezera_y": mezera_y}

# -------------------------------------------------------
# POMOCNÁ FUNKCE – PŘEHRÁNÍ ZVUKU (NEUPRAVUJTE)
# -------------------------------------------------------

def zahraj(zvuk_promenna):
    """Bezpečně přehraje zvuk – pokud není načten, nic se nestane."""
    try:
        zvuk_promenna.play()
    except NameError:
        pass

# -------------------------------------------------------
# HLAVNÍ HERNÍ SMYČKA
# -------------------------------------------------------

def hra():
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

                        # ============================================================
                        #  BLOK C – ZVUK SKOKU  ← VÁŠ ÚKOL
                        #
                        #  Přehrajte zvuk skoku pomocí funkce zahraj().
                        #
                        #  NÁPOVĚDA:
                        #    zahraj(zvuk_skok)
                        # ============================================================

                        # --- Sem napište přehrání zvuku skoku ---

                    else:
                        hra()
                        return

        # FYZIKA (hotové)
        if bezi:
            ptacek_vy += TIZEN
            ptacek_y  += ptacek_vy
            if ptacek_y - PTACEK_POLOMER < 0 or ptacek_y + PTACEK_POLOMER > VYSKA:
                bezi = False
                zahraj(zvuk_smrt)   # ← tento řádek je hotový jako ukázka

        # POHYB PILÍŘŮ (hotové z minula)
        if bezi:
            for pilir in pilire:
                pilir["x"] -= PILIR_RYCHLOST
            pilire = [p for p in pilire if p["x"] > -PILIR_SIRKA]
            if pilire[-1]["x"] < SIRKA - 200:
                pilire.append(vytvor_pilir())

        # KOLIZE A SKÓRE (hotové z minula)
        if bezi:
            for pilir in pilire:
                prekryv_x = (PTACEK_X + PTACEK_POLOMER > pilir["x"] and
                             PTACEK_X - PTACEK_POLOMER < pilir["x"] + PILIR_SIRKA)
                mimo_mezeru = (ptacek_y - PTACEK_POLOMER < pilir["mezera_y"] - PILIR_MEZERA // 2 or
                               ptacek_y + PTACEK_POLOMER > pilir["mezera_y"] + PILIR_MEZERA // 2)
                if prekryv_x and mimo_mezeru:
                    bezi = False

                    # ============================================================
                    #  BLOK D – ZVUK SMRTI  ← VÁŠ ÚKOL
                    #
                    #  Přehrajte zvuk smrti pomocí funkce zahraj().
                    #  (Narážka: je to stejné jako u zvuku skoku,
                    #   ale s jinou proměnnou.)
                    # ============================================================

                    # --- Sem napište přehrání zvuku smrti ---

                if pilir["x"] + PILIR_SIRKA // 2 == PTACEK_X:
                    skore += 1

                    # ============================================================
                    #  BLOK E – ZVUK BODU  ← VÁŠ ÚKOL
                    #
                    #  Přehrajte zvuk bodu pomocí funkce zahraj().
                    # ============================================================

                    # --- Sem napište přehrání zvuku bodu ---

        # VYKRESLENÍ (neupravujte)
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
hra()
pygame.quit()
