import pandas as pd
import re

df = pd.read_excel("jidla.xls", header=4)

# Sloupce, které chceme převést na čísla
numeric_cols = ["kcal", "Bílkoviny [g]", "Sacharidy [g]", "Cukry [g]", "Tuky [g]",
                "Nasycené mastné kyseliny [g]", "Trans mastné kyseliny [g]",
                "Cholesterol [mg]", "Vláknina [g]", "Sodík [mg]", "Vápník [g]", "PHE [mg]"]

# Funkce na převod textu na číslo
def clean_number(x):
    if pd.isna(x):
        return None
    x = str(x).replace(",", ".")
    x = "".join(c for c in x if c.isdigit() or c==".")
    try:
        return float(x)
    except:
        return None

for col in numeric_cols:
    df[col] = df[col].apply(clean_number)

# Funkce na převod množství a zachování jednotky
def parse_mnozstvi_with_unit(x):
    if pd.isna(x):
        return None
    x = str(x).replace(",", ".")
    # Najdeme čísla
    numbers = re.findall(r"[\d\.]+", x)
    # Najdeme jednotku (g, ml atd.)
    unit_match = re.search(r"(g|ml)", x)
    unit = unit_match.group(1) if unit_match else ""
    
    if len(numbers) == 2:
        total = float(numbers[0]) * float(numbers[1])
    elif len(numbers) == 1:
        total = float(numbers[0])
    else:
        return None
    
    return f"{total} {unit}"

# Přepíšeme původní sloupec Množství
df['Množství'] = df['Množství'].apply(parse_mnozstvi_with_unit)

# Odstranit řádky bez názvu nebo kcal
df = df.dropna(subset=["Název", "kcal"])

print(df.head())
