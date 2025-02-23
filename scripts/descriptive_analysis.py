# ##DESCRIPTIVE STATISTICS
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
dishes= pd.read_csv('data/processed/dishes.csv') 
menu= pd.read_csv('data/processed/menu.csv') 
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