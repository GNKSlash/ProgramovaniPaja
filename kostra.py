import tkinter as tk
from tkinter import messagebox

# === DATOVÉ SEZNAMY ===
predmety = ["Čeština", "Matematika", "Angličtina"]
jmena = []

# V 'znamky' bude pro každého studenta seznam 3 seznamů (podle předmětů):
# Např. znamky[0] = [ ["1", "1", "2"], ["1", "2"], ["1", "1"] ]
znamky = []

SOUBOR = "znamky.txt"

# === FUNKCE PRO PRÁCI SE SOUBORY A SEZNAMY ===

def nacti_data():
    """Načte studenty a jejich známky ze všech předmětů ze souboru."""
    jmena.clear()
    znamky.clear()
    
    # TODO 1: Otevři SOUBOR pro čtení ("r", encoding="utf-8")
    # Pro každý řádek v souboru:
    #   1. Odstraň konec řádku (.strip()) a rozděl řádek podle středníku: casti = radek.strip().split(";")
    #      (vznikne např. ["Anička", "1 1 2", "1 2", "1 1"])
    #   2. První položku (casti[0]) přidej do seznamu 'jmena'
    #   3. Vytvoř prázdný pomocný seznam: student_predmety = []
    #   4. Projdi zbytek 'casti' (od indexu 1 dál -> casti[1:]):
    #        - každý textový blok rozděl podle mezer (.split()) a přidej do 'student_predmety'
    #   5. Celý seznam 'student_predmety' přidej do hlavního seznamu 'znamky'
    pass


def uloz_data():
    """Uloží aktuální seznamy zpět do textového souboru."""
    # TODO 2: Otevři SOUBOR pro zápis ("w", encoding="utf-8")
    # Projdi všechny studenty (for i in range(len(jmena))):
    #   1. Vytvoř prázdný seznam: bloky_predmetu = []
    #   2. Projdi všechny seznamy známek i-tého studenta (for z_predmetu in znamky[i]):
    #        - spoj známky mezerou (" ".join(z_predmetu)) a přidej do 'bloky_predmetu'
    #   3. Spoj 'bloky_predmetu' středníkem: text_znamek = ";".join(bloky_predmetu)
    #   4. Zapiš do souboru řádek: f"{jmena[i]};{text_znamek}\n"
    
    messagebox.showinfo("Uloženo", "Známky ze všech předmětů byly uloženy!")


def ukaz_znamky():
    """Zobrazí známky vybraného studenta ze všech předmětů."""
    vyber = seznam_box.curselection()
    if not vyber:
        messagebox.showwarning("Pozor", "Nejdřív vyber studenta ze seznamu!")
        return
    
    index = vyber[0]
    
    # TODO 3: Získej jméno studenta (jmena[index]) a jeho seznam předmětů (znamky[index])
    # Sestav text do proměnné 'vypis', který začne třeba f"Student: {jmeno}\n\n"
    # Projdi předměty pomocí cyklu: for p in range(len(predmety)):
    #   - získej název předmětu: predmety[p]
    #   - získej známky z tohoto předmětu: studentovy_predmety[p]
    #   - spoj je čárkou (", ".join(...)) a přičti k textu 'vypis' (nezapomeň na \n na konci řádku)
    # Nakonec zobraz text pomocí: label_vypis.config(text=vypis)
    pass


def pridej_znamku():
    """Přidá novou známku vybranému studentovi do vybraného předmětu."""
    vyber = seznam_box.curselection()
    nova_znamka = vstup_znamka.get().strip()
    vybrany_predmet = promenna_predmet.get() # Např. "Matematika"
    
    if not vyber:
        messagebox.showwarning("Pozor", "Nejdřív vyber studenta!")
        return
    if nova_znamka not in ["1", "2", "3", "4", "5"]:
        messagebox.showwarning("Chyba", "Zadej platnou známku (1 až 5)!")
        return

    index_studenta = vyber[0]
    
    # TODO 4: Zjisti, na jaké pozici (0, 1 nebo 2) je 'vybrany_predmet' v seznamu 'predmety'
    # Nápověda: Použij predmety.index(vybrany_predmet)
    # Potom přidej 'nova_znamka' do správného seznamu:
    # znamky[index_studenta][index_predmetu].append(nova_znamka)
    
    vstup_znamka.delete(0, tk.END)
    ukaz_znamky()


# === GRAFICKÉ ROZHRANÍ (UŽ HOTOVÉ) ===
okno = tk.Tk()
okno.title("Mini Bakaláři - Více předmětů")
okno.geometry("500x380")
okno.config(padx=15, pady=15)

# Levá část - seznam studentů
tk.Label(okno, text="Seznam studentů:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
seznam_box = tk.Listbox(okno, height=14, width=20, font=("Arial", 11))
seznam_box.grid(row=1, column=0, rowspan=4, pady=5)

# Pravá část - ovládání a zobrazení
btn_zobraz = tk.Button(okno, text="Zobrazit vysvědčení", width=20, command=ukaz_znamky)
btn_zobraz.grid(row=1, column=1, padx=15, sticky="n")

label_vypis = tk.Label(okno, text="Vyber studenta a klikni\nna Zobrazit vysvědčení", font=("Arial", 11), justify="left", fg="blue")
label_vypis.grid(row=2, column=1, padx=15, sticky="w")

# Sekce pro přidání známky s výběrem předmětu
ramecek_pridat = tk.Frame(okno)
ramecek_pridat.grid(row=3, column=1, padx=15, sticky="w")

promenna_predmet = tk.StringVar(okno)
promenna_predmet.set(predmety[0]) # Výchozí předmět je první v seznamu
menu_predmet = tk.OptionMenu(ramecek_pridat, promenna_predmet, *predmety)
menu_predmet.pack(side="left")

vstup_znamka = tk.Entry(ramecek_pridat, width=4, font=("Arial", 11))
vstup_znamka.pack(side="left", padx=5)

btn_pridat = tk.Button(ramecek_pridat, text="Přidat", command=pridej_znamku)
btn_pridat.pack(side="left")

# Tlačítko pro uložení
btn_uloz = tk.Button(okno, text="Uložit změny do souboru", width=24, bg="#d1ffd1", command=uloz_data)
btn_uloz.grid(row=4, column=1, padx=15, sticky="s")

# Spuštění načtení dat
nacti_data()
for jmeno in jmena:
    seznam_box.insert(tk.END, jmeno)

okno.mainloop()
