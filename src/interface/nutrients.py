import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from src.interface.shared_data import chosen_products

base_dir = Path(__file__).resolve().parent.parent.parent
data_path = base_dir / 'data' / 'processed' / 'dishes.xlsx'

NUTRIENTS = [
    ("Calcium", "Calcium"),
    ("Fer", "Iron"),
    ("Protides", "Proteins"),
    ("Glucides", "Carbohydrates"),
    ("Lipides", "Fats"),
    ("Lipides satures", "Saturated Fats")
]

# Seuils réalistes pour filtrer les valeurs incohérentes
MAX_VALUES = {
    "Calcium": 1.5,         # g
    "Iron": 0.05,           # g
    "Proteins": 40,
    "Carbohydrates": 80,
    "Fats": 40,             # g
    "Saturated Fats": 25    # g
}

# Ingrédients à ignorer dans l'analyse nutritionnelle
IGNORED_INGREDIENTS = {
    "poivre", "sel", "épices", "épice", "herbes", "bouillon", "arômes",
    "muscade", "piment", "eau", "gélatine", "agar-agar", "colorant",
    "conservateur", "acidifiant", "acidifiant e330","vinaigre", "huile essentielle", "fumet", "eau minérale", 
    "sucre", "gomme", "épaississant", "levure", "bicarbonate",
    "épice curry", "épices diverses","thym entier", "persil", "pâte à tartiner noisette"
}

def show_nutrient_stats(allergens):
    try:
        df = pd.read_excel(data_path)
    except Exception as e:
        print(f"⚠️ Error loading data: {e}")
        return

    if allergens and 'product_allergen' in df.columns:
        plats_avec_allergene = df[
            df['product_allergen']
            .astype(str)
            .str.lower()
            .str.contains('|'.join(allergens), na=False)
        ]['dish_code'].unique()
        df = df[~df['dish_code'].isin(plats_avec_allergene)]

    # Supprimer les ingrédients inutiles
    if 'product_name' in df.columns:
        df = df[~df['product_name'].str.lower().isin(IGNORED_INGREDIENTS)]

    # Supprimer les plats sans aucun apport nutritionnel
    df = df[(df["Proteins"] > 0) | (df["Carbohydrates"] > 0) | (df["Fats"] > 0)]

    print(f"✅ {len(df['dish_name'].unique())} unique dishes available after filtering.")

    if df.empty:
        print("⚠️ No dishes available after applying filters.")
        return

    while True:
        print("\n📊 Nutrient Statistics Available:")
        for i, (_, en_name) in enumerate(NUTRIENTS, 1):
            print(f"{i}. {en_name}")

        choice = input("\nChoose a nutrient (1-6) or type 'back' to return: ").strip().lower()

        if choice == "back":
            return
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(NUTRIENTS):
                fr_name, en_name = NUTRIENTS[idx - 1]
                if en_name in df.columns:
                    df_cleaned = df[df[en_name] <= MAX_VALUES[en_name]]
                    plot_nutrient_chart(df_cleaned, en_name)
                else:
                    print(f"⚠️ The column '{en_name}' was not found in the data.")
            else:
                print("⚠️ Invalid number. Please choose between 1 and 6.")
        else:
            print("⚠️ Invalid input. Please enter a number or 'back'.")

def plot_nutrient_chart(df: pd.DataFrame, nutrient: str):
    try:
        if 'dish_name' not in df.columns or 'dish_code' not in df.columns:
            print("⚠️ 'dish_name' or 'dish_code' column is missing in the dataset.")
            return

        df_grouped = df.groupby("dish_name").agg(
            {nutrient: "sum", "dish_code": "nunique"}
        ).reset_index()

        df_grouped[nutrient] = df_grouped[nutrient] / df_grouped["dish_code"]

        top_dishes = df_grouped.sort_values(by=nutrient, ascending=False).head(10)

        plt.figure(figsize=(10, 6))
        sns.barplot(
            y=top_dishes['dish_name'],
            x=top_dishes[nutrient],
            palette="viridis",
            errorbar=None
        )
        plt.title(f"Top Dishes by {nutrient}", fontsize=14)
        plt.xlabel(f"{nutrient} (g per dish instance)", fontsize=12)
        plt.ylabel("Dish Name", fontsize=12)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"⚠️ Error generating chart: {e}")

def get_chosen_products_nutrients():
    dishes_file_path = base_dir / 'data' / 'processed' / 'dishes.xlsx'

    nutrient_columns = [
        "Proteins", "Carbohydrates", "Fats",
        "Saturated Fats", "Iron", "Calcium"
    ]

    try:
        df = pd.read_excel(dishes_file_path)
    except Exception as e:
        print(f"⚠️ Erreur pour charger {dishes_file_path}: {e}")
        return {}

    results = {}

    for index, (dish_index, dish_name, dish_type, included_ingredients, removed_ingredients) in enumerate(chosen_products, start=1):
        dish_rows = df[df["dish_name"] == dish_name]

        if included_ingredients:
            dish_rows = dish_rows[dish_rows["product_name"].isin(included_ingredients)]
        else:
            dish_rows = pd.DataFrame()

        if dish_rows.empty:
            results[f"{dish_name} ({index})"] = {col: 0 for col in nutrient_columns}
            continue

        grouped = dish_rows.groupby("dish_name").agg(
            {
                "Proteins": "sum",
                "Carbohydrates": "sum",
                "Fats": "sum",
                "Saturated Fats": "sum",
                "Iron": "sum",
                "Calcium": "sum",
                "dish_code": "nunique"
            }
        ).reset_index()

        row = grouped.iloc[0]
        code_count = row["dish_code"]
        nutrient_data = {col: round(row[col] / code_count, 2) for col in nutrient_columns}

        results[f"{dish_name} ({index})"] = nutrient_data

    return results

def display_chosen_products_nutrients():
    nutrients = get_chosen_products_nutrients()
    if not nutrients:
        print("\n⚠️ No nutrient data available.")
        return

    print("\nNutrient details for your chosen dishes:")
    for dish_name, nutrient_info in nutrients.items():
        print(f"\u2022 {dish_name}")
        for nutrient, value in nutrient_info.items():
            print(f"   - {nutrient}: {value}")
        print()
