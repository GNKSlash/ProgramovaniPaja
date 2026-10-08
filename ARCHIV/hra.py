import pygame
import random


# --- 1. NASTAVENÍ ---
pygame.init()
SIRKA, VYSKA = 800, 600
# Zvětšíme okno o 60 pixelů pro spodní lištu achievementů
platno = pygame.display.set_mode((SIRKA, VYSKA + 60)) 
pygame.display.set_caption("Moje hra s Achievementy")
hodiny = pygame.time.Clock()
stav_hry = "MENU"

# Barvy
CERNA = (0, 0, 0)
BILA = (255, 255, 255)
MODRA = (0, 0, 255)
ZLUTA = (255, 200, 0)
CERVENA = (255, 50, 50)
SEDA = (50, 50, 50)
ZELENA = (0, 255, 0)

# --- STATISTIKY PRO ACHIEVEMENTY ---
celkova_vzdalenost = 0
pocet_smrti = 0
celkem_minci = 0

# Definice achievementů (Písmeno, Název, Cíl, Aktuální hodnota - index do statistik)
# 0 = vzdálenost, 1 = smrti, 2 = mince
achv_list = [
    {"pismeno": "V", "ukol": "Ujdi 5000 m", "cil": 5000, "id": 0},
    {"pismeno": "S", "ukol": "Zemři 5x", "cil": 5, "id": 1},
    {"pismeno": "M", "ukol": "Nasbírej 10 mincí", "cil": 10, "id": 2}
]

# --- 2. TVORBA POSTAV ---
hrac = pygame.Rect(400, 300, 50, 50)
mince = pygame.Rect(random.randint(0, SIRKA - 50), random.randint(0, VYSKA - 50), 50, 50)
nepritel = pygame.Rect(50, 500, 90, 50)

rychlost_nepi = 3
rychlost_hrace = 5
skore = 0
max_skore = 0
game_over = False

font = pygame.font.SysFont("Arial", 24)
maly_font = pygame.font.SysFont("Arial", 18)
velky_font = pygame.font.SysFont("Arial", 64)

# --- HLAVNÍ SMYČKA ---
bezi = True
while bezi:
    pozice_mysi = pygame.mouse.get_pos()
    
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            bezi = False
        
        # Ovládání v MENU
        if stav_hry == "MENU":
            if udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_SPACE:
                    stav_hry = "HRA"
        
        # Ovládání ve hŘE (Restart)
        elif stav_hry == "SMRT":
            if udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_r and game_over:
                    # ... tvůj stávající kód pro restart ...
                    game_over = False
                    if skore > max_skore:
                        max_skore = skore
                    skore = 0
                    hrac.center = (400, 300)
                    stav_hry = "HRA" # Ujistíme se, že jsme ve hře
                    nepritel.center = (random.randint(0,SIRKA-50), random.randint(0,VYSKA-50))
                    rychlost_hrace = 5


    if stav_hry == "HRA":
        # --- 4. POHYB A STATISTIKY ---
        stare_x, stare_y = hrac.x, hrac.y
        
        klavesy = pygame.key.get_pressed()
        if klavesy[pygame.K_LEFT] or klavesy[pygame.K_a]:  hrac.x -= rychlost_hrace
        if klavesy[pygame.K_RIGHT] or klavesy[pygame.K_d]: hrac.x += rychlost_hrace
        if klavesy[pygame.K_DOWN] or klavesy[pygame.K_s]:  hrac.y += rychlost_hrace
        if klavesy[pygame.K_UP] or klavesy[pygame.K_w]:    hrac.y -= rychlost_hrace

        # Přičtení vzdálenosti (absolutní rozdíl pohybu)
        celkova_vzdalenost += abs(hrac.x - stare_x) + abs(hrac.y - stare_y)

        # Hranice obrazovky
        hrac.clamp_ip(pygame.Rect(0, 0, SIRKA, VYSKA))

        # --- 5. POHYB NEPŘÍTELE ---
        if hrac.x > nepritel.x: nepritel.x += rychlost_nepi
        elif hrac.x < nepritel.x: nepritel.x -= rychlost_nepi
        if hrac.y > nepritel.y: nepritel.y += rychlost_nepi
        elif hrac.y < nepritel.y: nepritel.y -= rychlost_nepi

        # --- 6. KOLIZE ---
        if hrac.colliderect(nepritel):
            game_over = True
            stav_hry = "SMRT"
            pocet_smrti += 1 # PŘIČTENÍ SMRTI

        if hrac.colliderect(mince):
            skore += 1
            celkem_minci += 1 # PŘIČTENÍ MINCE
            mince.x = random.randint(0, SIRKA - 50)
            mince.y = random.randint(0, VYSKA - 50)
            rychlost_hrace += 0.5

        # --- 7. KRESLENÍ ---
    platno.fill(CERNA)

    if stav_hry == "MENU":
        pass
    if stav_hry == "HRA":
        pygame.draw.rect(platno, MODRA, hrac)
        pygame.draw.rect(platno, ZLUTA, mince)
        pygame.draw.rect(platno, CERVENA, nepritel)
    if stav_hry == "SMRT":
        text = velky_font.render("GAME OVER", True, CERVENA)
        platno.blit(text, (SIRKA//2 - 150, 200))
        text_r = font.render("Zmáčkni R pro restart", True, BILA)
        platno.blit(text_r, (SIRKA//2 - 100, 300))

    if stav_hry != "MENU":
        # Horní UI
        text_skore = font.render(f"Skóre: {skore}  Max: {max_skore}", True, BILA)
        platno.blit(text_skore, (10, 10))
        #lista_rect = pygame.Rect(0, VYSKA, SIRKA, 60)
        #pygame.draw.rect(platno, SEDA, lista_rect)
        #pygame.draw.line(platno, BILA, (0, VYSKA), (SIRKA, VYSKA), 2)



    # --- LIŠTA ACHIEVEMENTŮ ---


    pygame.display.flip()
    hodiny.tick(60)

pygame.quit()
