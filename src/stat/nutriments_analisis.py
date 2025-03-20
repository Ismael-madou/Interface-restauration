import pandas as pd
import re
import matplotlib
matplotlib.use("TkAgg")  # Ouvrir une fenêtre indépendante

import matplotlib.pyplot as plt
import seaborn as sns


dishes= pd.read_excel('data/processed/dishes.xlsx') 
menu= pd.read_excel('data/processed/menu.xlsx') 
# 🔍 Vérifier le nom de la colonne nutriments
print(dishes.columns)
nutriment_col = "platProduitNutriment" if "platProduitNutriment" in dishes.columns else "product_nutrient"

# 🛠 Fonction pour extraire les nutriments
def extract_nutrient(nutriment_str, nutrient_name):
    if pd.isna(nutriment_str):
        return 0
    pattern = rf'([\d\.]+)(mg|g) {nutrient_name}'
    match = re.search(pattern, nutriment_str)
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        if unit == "mg":
            value /= 1000  # Convertir mg en g
        return value
    return 0

# 📌 Liste des nutriments
nutrients = ["Calcium", "Fer", "Protides", "Glucides", "Lipides", "Lipides satures"]

# 🏗 Appliquer l'extraction
for nutrient in nutrients:
    dishes[nutrient] = dishes[nutriment_col].astype(str).apply(lambda x: extract_nutrient(x, nutrient))

# 📊 Regrouper les nutriments par plat
nutrients_by_dish = dishes.groupby("dish_name")[nutrients].sum()

# 🎨 Affichage des graphiques avec barres horizontales
for nutrient in nutrients:
    plt.clf()
    plt.close('all')

    top_dishes = nutrients_by_dish[nutrient].sort_values(ascending=False).head(20)  # Top 20 plats

    fig_height = max(8, len(top_dishes) * 0.5)  # Ajuster hauteur pour affichage propre
    plt.figure(figsize=(12, fig_height))  # 📌 Ajuster la largeur et la hauteur
    plt.subplots_adjust(left=0.4)  # Augmenter la marge à gauche (valeur entre 0 et 1)

    sns.barplot(y=top_dishes.index, x=top_dishes.values, palette="viridis", orient='h')  # 📌 BAR CHART HORIZONTAL

    plt.title(f"Quantité totale de {nutrient} par plat", fontsize=14)
    plt.ylabel("Nom du plat", fontsize=12)  # 📌 Axe Y pour les noms des plats
    plt.xlabel(f"{nutrient} (g)", fontsize=12)

    plt.xticks(fontsize=12)  # Ajuste la taille des valeurs
    plt.yticks(fontsize=12)  # 📌 Les noms des plats seront enfin bien affichés !

    plt.show()
    plt.close()

