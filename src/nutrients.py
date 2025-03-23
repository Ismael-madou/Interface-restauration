import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from shared_data import chosen_products


# Define path to the Excel data file
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'data' / 'processed' / 'dishes.xlsx'

# List of nutrients to analyze (French, English)
NUTRIENTS = [
    ("Calcium", "Calcium"),
    ("Fer", "Iron"),
    ("Protides", "Proteins"),
    ("Glucides", "Carbohydrates"),
    ("Lipides", "Fats"),
    ("Lipides satures", "Saturated Fats")
]

def show_nutrient_stats(allergens):
    """
    Display available nutrients and allow the user to select one for charting.
    Filter out any dishes that contain at least one allergenic product.

    Args:
        allergens (List[str]): List of allergens to avoid.
    """
    try:
        # Load the dish data from Excel
        df = pd.read_excel(DATA_PATH)
    except Exception as e:
        print(f"⚠️ Error loading data: {e}")
        return

    # If allergen filtering is required
    if allergens:
        if 'product_allergen' not in df.columns:
            print("⚠️ Warning: No allergen information found in dataset.")
        else:
            # Identify dishes containing at least one allergenic product
            plats_avec_allergene = df[
                df['product_allergen']
                .astype(str)
                .str.lower()
                .str.contains('|'.join(allergens), na=False)
            ]['dish_code'].unique()

            # Exclude those dishes from the DataFrame
            df = df[~df['dish_code'].isin(plats_avec_allergene)]

    # Show the number of dishes that are allergen-safe
    print(f"✅ {len(df['dish_name'].unique())} unique dishes available after filtering out allergenic products.")

    if df.empty:
        print("⚠️ No dishes available after applying allergen filters.")
        return

    # Display a menu to the user to choose which nutrient to visualize
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
                    # Proceed to generate the graph
                    plot_nutrient_chart(df, en_name)
                else:
                    print(f"⚠️ The column '{en_name}' was not found in the data.")
            else:
                print("⚠️ Invalid number. Please choose between 1 and 6.")
        else:
            print("⚠️ Invalid input. Please enter a number or 'back'.")

def plot_nutrient_chart(df: pd.DataFrame, nutrient: str):
    """
    Plot a horizontal bar chart showing the top dishes ranked by a given nutrient.
    Aggregate values by dish name and divide by the number of unique dish codes for accuracy.
    
    Args:
        df (pd.DataFrame): Filtered dish dataset.
        nutrient (str): Name of the nutrient column to analyze.
    """
    try:
        if 'dish_name' not in df.columns or 'dish_code' not in df.columns:
            print("⚠️ 'dish_name' or 'dish_code' column is missing in the dataset.")
            return

        # Aggregate nutrient totals by dish name
        df_grouped = df.groupby("dish_name").agg(
            {nutrient: "sum", "dish_code": "nunique"}  # Count distinct dish codes per dish name
        ).reset_index()

        # Compute the average nutrient content per dish instance
        df_grouped[nutrient] = df_grouped[nutrient] / df_grouped["dish_code"]

        # Sort dishes by nutrient value in descending order and select the top
        top_dishes = df_grouped.sort_values(by=nutrient, ascending=False).head(10)

        # Plot horizontal bar chart for visual comparison
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
    import pandas as pd
    from pathlib import Path
    from shared_data import chosen_products

    base_dir = Path(__file__).resolve().parent.parent
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

    # Ajoute un numéro unique à chaque plat pour éviter d'écraser les doublons
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

        # On ajoute l'index unique au nom du plat pour éviter l'écrasement
        results[f"{dish_name} ({index})"] = nutrient_data

    return results


def display_chosen_products_nutrients():
    nutrients = get_chosen_products_nutrients()
    if not nutrients:
        print("\n⚠️ No nutrient data available.")
        return

    print("\nNutrient details for your chosen dishes:")
    for dish_name, nutrient_info in nutrients.items():
        print(f"• {dish_name}")
        for nutrient, value in nutrient_info.items():
            print(f"   - {nutrient}: {value}")
        print()
