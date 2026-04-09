import pygame
import random

pygame.init()

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
okno = pygame.display.set_mode((SIRKA, VYSKA))
pygame.display.set_caption("Flappy Bird")
hodiny = pygame.time.Clock()
font_velky  = pygame.font.SysFont("Arial", 52, bold=True)
font_maly   = pygame.font.SysFont("Arial", 28)

# -------------------------------------------------------
# POMOCNÉ FUNKCE
# -------------------------------------------------------

def nakresli_ptacka(povrch, y):
    pygame.draw.circle(povrch, BARVA_PTACEK, (PTACEK_X, int(y)), PTACEK_POLOMER)
    pygame.draw.circle(povrch, (200, 160, 0), (PTACEK_X, int(y)), PTACEK_POLOMER, 3)

def nakresli_pilire(povrch, pilire):
    for pilir in pilire:
        horni_vyska   = pilir["mezera_y"] - PILIR_MEZERA // 2
        dolni_zacatek = pilir["mezera_y"] + PILIR_MEZERA // 2
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
                    else:
                        hra()
                        return

        # ============================================================
        #  BLOK 1 – FYZIKA PTÁČKA (hotové)
        # ============================================================
        if bezi:
            ptacek_vy += TIZEN
            ptacek_y  += ptacek_vy

            if ptacek_y - PTACEK_POLOMER < 0 or ptacek_y + PTACEK_POLOMER > VYSKA:
                bezi = False

        # ============================================================
        #  BLOK 2 – POHYB PILÍŘŮ  ✓ ŘEŠENÍ
        # ============================================================
        if bezi:
            # 1) Posuň každý pilíř doleva
            for pilir in pilire:
                pilir["x"] -= PILIR_RYCHLOST

            # 2) Odstraň pilíře, které vyletěly z obrazovky
            pilire = [p for p in pilire if p["x"] > -PILIR_SIRKA]

            # 3) Přidej nový pilíř, když je poslední dost daleko
            if pilire[-1]["x"] < SIRKA - 200:
                pilire.append(vytvor_pilir())

        # ============================================================
        #  BLOK 3 – KOLIZE A SKÓRE  ✓ ŘEŠENÍ
        # ============================================================
        if bezi:
            for pilir in pilire:
                # Vodorovný překryv ptáčka s pilířem?
                prekryv_x = (PTACEK_X + PTACEK_POLOMER > pilir["x"] and
                             PTACEK_X - PTACEK_POLOMER < pilir["x"] + PILIR_SIRKA)

                # Svislý překryv – ptáček mimo mezeru?
                mimo_mezeru = (ptacek_y - PTACEK_POLOMER < pilir["mezera_y"] - PILIR_MEZERA // 2 or
                               ptacek_y + PTACEK_POLOMER > pilir["mezera_y"] + PILIR_MEZERA // 2)

                if prekryv_x and mimo_mezeru:
                    bezi = False

                # Bod za průlet – střed pilíře právě minul ptáčka
                if pilir["x"] + PILIR_SIRKA // 2 == PTACEK_X:
                    skore += 1

        # ============================================================
        #  VYKRESLENÍ
        # ============================================================
        okno.fill(BARVA_POZADI)
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
