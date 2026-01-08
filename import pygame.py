import pygame
import random

# --- 1. NASTAVENÍ (PŘEDCHYSTÁNO) ---
pygame.init()
SIRKA, VYSKA = 800, 600
platno = pygame.display.set_mode((SIRKA, VYSKA))
pygame.display.set_caption("Moje hra")
hodiny = pygame.time.Clock()

# Barvy
CERNA = (0, 0, 0)
BILA = (255, 255, 255)
MODRA = (0, 120, 255)
ZLUTA = (255, 200, 0)
CERVENA = (255, 50, 50)

# --- 2. TVORBA POSTAV (ÚKOLY) ---

# ÚKOL: Vytvoř hráče pomocí pygame.Rect na souřadnicích 400, 300
hrac = 1# DOPLŇ ZDE

# ÚKOL: Vytvoř minci na náhodném místě (použij random.randint)
mince = 1# DOPLŇ ZDE

# ÚKOL: Vytvoř nepřítele
nepritel = 1# DOPLŇ ZDE
rychlost_nepi = [3, 3]

# Proměnné pro stav hry
skore = 0
game_over = False
font = pygame.font.SysFont("Arial", 32)

# --- HLAVNÍ SMYČKA ---
bezi = True
while bezi:
    # --- 3. UDÁLOSTI (ZAVŘENÍ OKNA A RESTART) ---
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            bezi = False
        
        # ÚKOL: Pokud je game_over a hráč stiskne klávesu R, resetuj hru
        # Hint: hrac.x = 400, skore = 0, game_over = False
        if udalost.type == pygame.KEYDOWN:
            pass # DOPLŇ LOGIKU RESTARTU ZDE

    if not game_over:
        # --- 4. POHYB HRÁČE ---
        klavesy = pygame.key.get_pressed()
        # ÚKOL: Rozpohybuj hráče pomocí šipek (K_LEFT, K_RIGHT, K_UP, K_DOWN)
        # Hint: měň hodnoty hrac.x a hrac.y
        # DOPLŇ ZDE


        # --- 5. POHYB NEPŘÍTELE ---
        # ÚKOL: Přičítej k nepritel.x a nepritel.y jeho rychlost
        # DOPLŇ ZDE

        # ÚKOL: Pokud nepřítel narazí do kraje obrazovky, odraz ho (otoč znaménko rychlosti)
        # Hint: if nepritel.left < 0 or nepritel.right > SIRKA: ...
        # DOPLŇ ZDE


        # --- 6. KOLIZE (SBÍRÁNÍ A SMRT) ---
        # ÚKOL: Zjisti, zda se hráč dotkl mince
        # Hint: použij hrac.colliderect(mince)
        # Pokud ano: zvyš skore o 1 a dej minci na nové náhodné místo
        # DOPLŇ ZDE


        # ÚKOL: Zjisti, zda se hráč dotkl nepřítele
        # Pokud ano: nastav game_over = True
        # DOPLŇ ZDE


    # --- 7. KRESLENÍ NA OBRAZOVKU ---
    platno.fill(CERNA) # Vyčištění plochy

    if not game_over:
        # ÚKOL: Nakresli hráče (MODRA) a nepřítele (CERVENA) jako obdélníky
        # Hint: pygame.draw.rect(platno, BARVA, OBJEKT)
        # DOPLŇ ZDE

        # ÚKOL: Nakresli minci (ZLUTA) jako elipsu (kruh)
        # Hint: pygame.draw.ellipse(platno, ZLUTA, mince)
        # DOPLŇ ZDE

        # ÚKOL: Vypiš skóre (Těžší úkol)
        # Hint: text = font.render(str(skore), True, BILA)
        # platno.blit(text, (10, 10))
        # DOPLŇ ZDE
        pass
    else:
        pass
        # ÚKOL: Vypiš text "GAME OVER - Stiskni R"
        # DOPLŇ ZDE
        

    pygame.display.flip() # Překreslení obrazovky
    hodiny.tick(60)       # Rychlost hry (60 snímků za sekundu)

pygame.quit()
