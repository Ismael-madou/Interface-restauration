# ##DESCRIPTIVE STATISTICS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
dishes= pd.read_csv('data/processed/dishes.xlsx') 
menu= pd.read_csv('data/processed/menu.xlsx') 
print(dishes["product_allergen"].unique())
print(dishes['product_nutrient'].value_counts())


allergen_dish_counts = dishes.groupby('product_allergen')['dish_name'].nunique()
print(allergen_dish_counts)
dish_counts = dishes['dish_name'].value_counts()
print(dish_counts)

# Mapping dish names to shorter numeric labels
dish_mapping = {dish: idx for idx, dish in enumerate(dish_counts.index, start=1)}

# Replace dish names with numeric labels
dish_counts_mapped = dish_counts.rename(index=dish_mapping)

# Set Seaborn style for better visualization
sns.set_style("whitegrid")
plt.figure(figsize=(13, 6))

# Barplot using numeric labels
sns.barplot(x=dish_counts_mapped.index, y=dish_counts_mapped.values, palette="viridis")

# Titles and axis labels
plt.title('Dish Frequency', fontsize=14)
plt.xlabel('Dish (Mapped)', fontsize=12)
plt.ylabel('Number of Occurrences', fontsize=12)

# Adjust x-axis ticks
plt.xticks(rotation=90, ha='right', fontsize=8)

# Add a legend with the mapping of dish numbers to names
legend_labels = [f"{num}: {name}" for name, num in dish_mapping.items()]
plt.legend(legend_labels, title="Dish Mapping", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=7, ncol=2)

# Adjust layout to fit everything properly
plt.tight_layout()
plt.show()

# Dictionary for mapping allergens to numbers
allergen_mapping = {allergen: i+1 for i, allergen in enumerate(allergen_dish_counts.keys())}

# replace allergen names by numbers for a better representation
mapped_index = [allergen_mapping[allergen] for allergen in allergen_dish_counts.keys()]
values = list(allergen_dish_counts.values)

# barplot 
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=mapped_index, y=values, palette="viridis")

plt.title('Number of dishes per allergen')
plt.xlabel('Allergen (mapped to numbers)')
plt.ylabel('Number of unique dishes')

# mapping allergens
legend_labels = [f"{num} → {name}" for name, num in allergen_mapping.items()]
plt.legend(legend_labels, title="Allergen Mapping", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=6, title_fontsize=10)

# Adjust layout to fit everything properly
plt.tight_layout()  

plt.xticks(mapped_index, mapped_index, rotation=45, ha='right')

plt.show()



###Cross tables 
pd.crosstab(dishes["dish_name"], dishes["product_allergen"])
pd.crosstab(menu["meal_type"], menu["dish_type"])


menu.groupby("menurestaurant_type")["dish_name"].count()
menu.groupby("menurestaurant_type")["dish_type"].nunique()
menu.groupby("meal_type")["dish_type"].value_counts()
