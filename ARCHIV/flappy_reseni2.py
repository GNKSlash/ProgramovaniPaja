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

BARVA_POZADI  = (113, 197, 207)
BARVA_PTACEK  = (255, 220, 50)
BARVA_PILIR   = (100, 200, 80)
BARVA_TEXT    = (255, 255, 255)



# -------------------------------------------------------
# INICIALIZACE OKNA
# -------------------------------------------------------
okno = pygame.display.set_mode((SIRKA, VYSKA), pygame.NOFRAME)
pygame.display.set_caption("Flappy Bird")
hodiny = pygame.time.Clock()
font_velky = pygame.font.SysFont("Arial", 52, bold=True)
font_maly  = pygame.font.SysFont("Arial", 28)

# -------------------------------------------------------
# STRUKTURA SLOŽEK
#
#  flappy/
#  ├── flappy_reseni2.py     ← tento soubor
#  ├── obrazky/
#  │   ├── pozadi.png        (400 × 600 px)
#  │   ├── ptacek.png        (36 × 36 px, průhledné PNG)
#  │   └── pilir.png         (60 × 600 px, průhledné PNG)
#  └── zvuky/
#      ├── skok.wav
#      ├── bod.wav
#      └── smrt.wav
# -------------------------------------------------------

# ============================================================
#  BLOK A – NAČTENÍ OBRÁZKŮ  ✓ ŘEŠENÍ
# ============================================================
img_pozadi = pygame.image.load("obrazky/pozadi.png").convert_alpha()
img_pozadi = pygame.transform.scale(img_pozadi, (SIRKA, VYSKA))

img_ptacek = pygame.image.load("obrazky/ptacek.png").convert_alpha()
img_ptacek = pygame.transform.scale(img_ptacek, (36, 36))

img_pilir  = pygame.image.load("obrazky/pilir.png").convert_alpha()
img_pilir  = pygame.transform.scale(img_pilir, (PILIR_SIRKA, VYSKA))

# ============================================================
#  BLOK B – NAČTENÍ ZVUKŮ  ✓ ŘEŠENÍ
# ============================================================
#zvuk_skok = pygame.mixer.Sound("zvuky/skok.wav")
#zvuk_bod  = pygame.mixer.Sound("zvuky/bod.wav")
#zvuk_smrt = pygame.mixer.Sound("zvuky/smrt.wav")

#zvuk_skok.set_volume(0.5)
#zvuk_bod.set_volume(0.7)
#zvuk_smrt.set_volume(0.8)



# -------------------------------------------------------
# POMOCNÉ FUNKCE
# -------------------------------------------------------

def nakresli_pozadi(povrch):
    try:
        povrch.blit(img_pozadi, (0, 0))
    except NameError:
        povrch.fill(BARVA_POZADI)

def nakresli_ptacka(povrch, y):
    try:
        povrch.blit(img_ptacek, (PTACEK_X - 18, int(y) - 18))
    except NameError:
        pygame.draw.circle(povrch, BARVA_PTACEK, (PTACEK_X, int(y)), PTACEK_POLOMER)
        pygame.draw.circle(povrch, (200, 160, 0), (PTACEK_X, int(y)), PTACEK_POLOMER, 3)

def nakresli_pilire(povrch, pilire):
    for pilir in pilire:
        horni_vyska   = pilir["mezera_y"] - PILIR_MEZERA // 2
        dolni_zacatek = pilir["mezera_y"] + PILIR_MEZERA // 2
        try:
            horni = pygame.transform.flip(img_pilir, False, True)
            horni = pygame.transform.scale(horni, (PILIR_SIRKA, horni_vyska))
            povrch.blit(horni, (pilir["x"], 0))
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

def zahraj(zvuk_promenna):
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
                        #  BLOK C – ZVUK SKOKU  ✓ ŘEŠENÍ
                        # ============================================================
                        #zahraj(zvuk_skok)

                    else:
                        hra()
                        return

        # FYZIKA
        if bezi:
            ptacek_vy += TIZEN
            ptacek_y  += ptacek_vy
            if ptacek_y - PTACEK_POLOMER < 0 or ptacek_y + PTACEK_POLOMER > VYSKA:
                bezi = False
                #zahraj(zvuk_smrt)

        # POHYB PILÍŘŮ
        if bezi:
            for pilir in pilire:
                pilir["x"] -= PILIR_RYCHLOST
            pilire = [p for p in pilire if p["x"] > -PILIR_SIRKA]
            if pilire[-1]["x"] < SIRKA - 200:
                pilire.append(vytvor_pilir())

        # KOLIZE A SKÓRE
        if bezi:
            for pilir in pilire:
                prekryv_x = (PTACEK_X + PTACEK_POLOMER > pilir["x"] and
                             PTACEK_X - PTACEK_POLOMER < pilir["x"] + PILIR_SIRKA)
                mimo_mezeru = (ptacek_y - PTACEK_POLOMER < pilir["mezera_y"] - PILIR_MEZERA // 2 or
                               ptacek_y + PTACEK_POLOMER > pilir["mezera_y"] + PILIR_MEZERA // 2)

                if prekryv_x and mimo_mezeru:
                    bezi = False

                    # ============================================================
                    #  BLOK D – ZVUK SMRTI  ✓ ŘEŠENÍ
                    # ============================================================
                    #zahraj(zvuk_smrt)

                if pilir["x"] + PILIR_SIRKA // 2 == PTACEK_X:
                    skore += 1

                    # ============================================================
                    #  BLOK E – ZVUK BODU  ✓ ŘEŠENÍ
                    # ============================================================
                    #zahraj(zvuk_bod)

        # VYKRESLENÍ
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
