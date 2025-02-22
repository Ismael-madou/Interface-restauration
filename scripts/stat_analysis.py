import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
import os

# Défine file path
BASE_DIR = Path(os.getcwd())  
print(BASE_DIR)
DATABASE_DIR = BASE_DIR / "Databases"  # excel file repository


menu = pd.read_excel(DATABASE_DIR / "antibes-menu-2025.xlsx")
dishes = pd.read_excel(DATABASE_DIR / "antibes-plats-2025.xlsx")

####DATA CLEANSE
#menu dataset cleaning
print(menu.head)
print(menu.info)
print(menu.describe)
print(menu.isnull().sum())

print(menu.shape)
print(menu.head().T) 
new_columns = ["menuRestaurantId","menuRestaurantType","menuRepasType","menuPlatType","menuPlatCode","menuPlatNom", "menuPlatAllergene",
"menuPlatLabel","menuPlatRegime"]  
menu = menu[new_columns]
print(menu.shape)  # 
print(menu.head())

print(menu.dtypes)
print(menu.head().T) 
print(menu.columns)
print(f"Columns : {menu.shape[1]}")
menu["menuPlatLabel"].fillna("Non renseigné", inplace=True)
menu["menuPlatAllergene"].fillna("Aucun", inplace=True)

# Dictionary to map old column names to new column 
print(menu.columns)
names = {
    "menuRestaurantId": "menurestaurant_id",
    "menuRestaurantType": "menurestaurant_type",
    "menuRepasType": "meal_type",
    "menuPlatType": "dish_type",
    "menuPlatCode": "dish_code",
    "menuPlatNom": "dish_name",
    "menuPlatAllergene": "dish_allergen",
    "menuPlatLabel": "dish_label",
    "menuPlatRegime": "dish_diet"
}

# Rename columns using the dictionary
menu.rename(columns=names, inplace=True)

# Display the first few rows to verify the changes
print(menu.head())
print(menu.head().T)
print(menu["dish_allergen"].unique())
print(menu["dish_label"].unique())



#dishes dataset cleaning
print(dishes.head)
print(dishes.info)
print(dishes.describe)
print(dishes.isnull().sum())

print(dishes.shape)
print(dishes.head().T) 

dishes_columns = ["platCode","platNom","platProduitNom","platProduitDescription","platProduitIonisation",
"platProduitAdditif", "platProduitAllergene",
"platProduitNutriment"] 
dishes = dishes[dishes_columns]
print(dishes.shape)
print(dishes.isnull().sum())
dishes = dishes.drop("platProduitIonisation", axis=1)
dishes = dishes.drop("platProduitAdditif", axis=1)
dishes["platProduitNutriment"].fillna("Non renseigné", inplace=True)
dishes["platProduitAllergene"].fillna("Aucun", inplace=True)
print(dishes["platProduitAllergene"].unique())
dishes["platProduitDescription"].fillna("Non renseigné", inplace=True)

 #Dictionary to map old column names to new column 
new_names = {
    "platCode": "dish_code",
    "platNom": "dish_name",
    "platProduitNom": "product_name",
    "platProduitDescription": "product_description",
    "platProduitAllergene": "product_allergen",
    "platProduitNutriment": "product_nutrient"
}

# Rename
dishes.rename(columns=new_names, inplace=True)
print(dishes.columns)

# ##DESCRIPTIVE STATISTICS 
 
print(dishes["product_allergen"].unique())
print(dishes['product_nutrient'].value_counts())


allergen_dish_counts = dishes.groupby('product_allergen')['dish_name'].nunique()
print(allergen_dish_counts)
dish_counts = dishes['dish_name'].value_counts()

# Barplot 
sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))


sns.barplot(x=dish_counts.index, y=dish_counts.values, palette="viridis")


plt.title('Dish Frequency', fontsize=14)
plt.xlabel('Dish Name', fontsize=12)
plt.ylabel('Number of Occurrences', fontsize=12)

plt.xticks(rotation=30, ha='right', fontsize=10)

plt.tight_layout()
plt.show()


import textwrap
plt.figure(figsize=(14, 6))
sns.barplot(x=allergen_dish_counts.index, y=allergen_dish_counts.values)
plt.title('Number of dishes per allergen')
plt.xlabel('Allergen')
plt.ylabel('Number of unique dishes')
#labels = [textwrap.fill(label, width=10) for label in allergen_dish_counts.index]
#plt.xticks(range(len(labels)), labels, rotation=45, ha='right', fontsize=8)
plt.xticks(rotation=45, ha='right',fontsize=8) 
#plt.tight_layout()
plt.show()

###Cross tables 
pd.crosstab(dishes["dish_name"], dishes["product_allergen"])
pd.crosstab(menu["meal_type"], menu["dish_type"])


menu.groupby("menurestaurant_type")["dish_name"].count()
menu.groupby("menurestaurant_type")["dish_type"].nunique()
menu.groupby("meal_type")["dish_type"].value_counts()

print(menu["menuPlatNom"].value_counts(normalize=True) * 100)