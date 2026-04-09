import pygame
import random

pygame.init()

# -------------------------------------------------------
# NASTAVENÍ HRY
# -------------------------------------------------------
SIRKA = 400
VYSKA = 600
FPS = 60

PTACEK_X = 80          # vodorovná pozice ptáčka (nemění se)
PTACEK_POLOMER = 18    # poloměr ptáčka
TIZEN = 0.5            # jak silně táhne gravitace dolů
SKOK = -10             # rychlost při skoku nahoru

PILIR_SIRKA = 60       # šířka pilíře
PILIR_MEZERA = 160     # výška mezery mezi horním a dolním pilířem
PILIR_RYCHLOST = 3     # jak rychle se pilíře posouvají doleva

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
# POMOCNÉ FUNKCE (NEUPRAVUJTE)
# -------------------------------------------------------

def nakresli_ptacka(povrch, y):
    """Nakreslí žlutý kroužek – ptáčka."""
    pygame.draw.circle(povrch, BARVA_PTACEK, (PTACEK_X, int(y)), PTACEK_POLOMER)
    pygame.draw.circle(povrch, (200, 160, 0), (PTACEK_X, int(y)), PTACEK_POLOMER, 3)

def nakresli_pilire(povrch, pilire):
    """Nakreslí všechny pilíře ze seznamu."""
    for pilir in pilire:
        # pilir je slovník: {"x": ..., "mezera_y": ...}
        # mezera_y = střed mezery (kde ptáček může prolétnout)
        horni_vyska  = pilir["mezera_y"] - PILIR_MEZERA // 2
        dolni_zacatek = pilir["mezera_y"] + PILIR_MEZERA // 2

        # horní pilíř
        pygame.draw.rect(povrch, BARVA_PILIR,
                         (pilir["x"], 0, PILIR_SIRKA, horni_vyska))
        # dolní pilíř
        pygame.draw.rect(povrch, BARVA_PILIR,
                         (pilir["x"], dolni_zacatek, PILIR_SIRKA, VYSKA - dolni_zacatek))

def nakresli_skore(povrch, skore):
    """Zobrazí skóre v horní části obrazovky."""
    text = font_velky.render(str(skore), True, BARVA_TEXT)
    povrch.blit(text, (SIRKA // 2 - text.get_width() // 2, 30))

def obrazovka_konec(povrch, skore):
    """Obrazovka po skončení hry."""
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
    """Vrátí nový pilíř s náhodnou výškou mezery."""
    mezera_y = random.randint(150, VYSKA - 150)
    return {"x": SIRKA, "mezera_y": mezera_y}

# -------------------------------------------------------
# HLAVNÍ HERNÍ SMYČKA
# -------------------------------------------------------

def hra():
    # --- Počáteční hodnoty ---
    ptacek_y  = VYSKA // 2    # svislá poloha ptáčka
    ptacek_vy = 0             # svislá rychlost ptáčka
    skore     = 0
    bezi      = True          # True = hra běží, False = konec
    pilire    = [vytvor_pilir()]  # seznam pilířů

    while True:
        hodiny.tick(FPS)

        # === OBSLUHA UDÁLOSTÍ ===
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                return

            if udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_SPACE:
                    if bezi:
                        # --- SKOK ---
                        ptacek_vy = SKOK
                    else:
                        # Restart hry
                        hra()
                        return

        # ============================================================
        #  BLOK 1 – FYZIKA PTÁČKA
        #  Tato část je hotová. Podívejte se, jak funguje gravitace.
        # ============================================================
        if bezi:
            ptacek_vy += TIZEN       # gravitace zrychluje pád
            ptacek_y  += ptacek_vy   # posun o aktuální rychlost

            # Ptáček vyletěl ven nebo dopadl na zem → konec
            if ptacek_y - PTACEK_POLOMER < 0 or ptacek_y + PTACEK_POLOMER > VYSKA:
                bezi = False

        # ============================================================
        #  BLOK 2 – POHYB PILÍŘŮ  ← VÁŠ ÚKOL
        #
        #  Pro každý pilíř v seznamu "pilire":
        #    1) Posuňte pilíř doleva o PILIR_RYCHLOST
        #
        #    2) Pokud pilíř vyletěl zcela z obrazovky (x < -PILIR_SIRKA),
        #       odstraňte ho ze seznamu.
        #
        #    3) Pokud poslední pilíř v seznamu je dál než 200 pixelů od
        #       pravého okraje, přidejte nový pilíř pomocí vytvor_pilir().
        #
        #  NÁPOVĚDA: Nový seznam bez starých pilířů vytvoříte takto:
        #    pilire = [p for p in pilire if p["x"] > -PILIR_SIRKA]
        # ============================================================

        # --- Sem napište svůj kód pro Blok 2 ---


        # ============================================================
        #  BLOK 3 – KOLIZE A SKÓRE  ← VÁŠ ÚKOL
        #
        #  Pro každý pilíř zkontrolujte, zda se ptáček srazil:
        #
        #  Kolize VODOROVNĚ nastane, když:
        #    ptacek_x (= PTACEK_X) + PTACEK_POLOMER > pilir["x"]
        #    A ZÁROVEŇ
        #    ptacek_x (= PTACEK_X) - PTACEK_POLOMER < pilir["x"] + PILIR_SIRKA
        #
        #  Kolize SVISLE nastane, když ptáček NENÍ v mezeře:
        #    ptacek_y - PTACEK_POLOMER < pilir["mezera_y"] - PILIR_MEZERA // 2
        #    NEBO
        #    ptacek_y + PTACEK_POLOMER > pilir["mezera_y"] + PILIR_MEZERA // 2
        #
        #  Pokud nastane OBOJÍ → nastavte bezi = False
        #
        #  SKÓRE: Pokud střed pilíře právě prošel ptáčkem
        #  (pilir["x"] + PILIR_SIRKA // 2 == PTACEK_X), přičtěte 1 bod.
        # ============================================================

        # --- Sem napište svůj kód pro Blok 3 ---


        # ============================================================
        #  VYKRESLENÍ  (NEUPRAVUJTE)
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
