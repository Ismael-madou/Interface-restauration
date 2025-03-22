import pandas as pd
import re

# Charger le fichier Excel
file_path = "data/processed/dishesancien.xlsx"
df = pd.read_excel(file_path)

# Vérifier la colonne contenant les nutriments
nutrient_col = "product_nutriment" if "product_nutriment" in df.columns else "platProduitNutriment"

# Dictionnaire de traduction des noms de nutriments
nutrients_translation = {
    "Calcium": "Calcium",
    "Fer": "Iron",
    "Protides": "Proteins",
    "Glucides": "Carbohydrates",
    "Lipides": "Fats",
    "Lipides satures": "Saturated Fats"
}

# Fonction pour extraire les nutriments
def extract_nutrient(nutriment_str, nutrient_name):
    if pd.isna(nutriment_str):
        return 0  # Mettre 0 si aucune donnée

    # Recherche du nutriment dans la chaîne
    pattern = rf'([\d\.]+)(mg|g) {nutrient_name}'
    match = re.search(pattern, nutriment_str)
    
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        if unit == "mg":
            value /= 1000  # Convertir mg en g
        return value
    return 0  # Si non trouvé, mettre 0

# Sélectionner uniquement les colonnes A à E
df_cleaned = df.iloc[:, :5].copy()  # Prend A à E

# Ajouter les nouvelles colonnes pour les nutriments avec noms en anglais
for fr_nutrient, en_nutrient in nutrients_translation.items():
    df_cleaned[en_nutrient] = df[nutrient_col].astype(str).apply(lambda x: extract_nutrient(x, fr_nutrient))

# Remplacer les valeurs NaN dans les colonnes de nutriments par 0
df_cleaned[list(nutrients_translation.values())] = df_cleaned[list(nutrients_translation.values())].fillna(0)

# Enregistrer le fichier nettoyé
output_file = "data/processed/dishes_cleaned.xlsx"
df_cleaned.to_excel(output_file, index=False, engine='openpyxl')

print(f"✅ Fichier nettoyé enregistré sous : {output_file}")
