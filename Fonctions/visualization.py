# install : pip install matplotlib seaborn before running the program
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from shared_data import chosen_products

def plot_most_ordered_dishes():
    """
    Generates a bar chart of the most ordered dishes based on the user's choices.

    This function uses the `chosen_products` list to count the frequency of each dish
    and displays a bar chart showing the most popular dishes.
    """
    if not chosen_products:
        print("No data available to generate the chart.")
        return


    dishes = [product[1] for product in chosen_products]


    dish_counts = Counter(dishes)

    sorted_dishes = sorted(dish_counts.items(), key=lambda x: x[1], reverse=True)

    dish_names = [dish[0] for dish in sorted_dishes]
    dish_frequencies = [dish[1] for dish in sorted_dishes]

    plt.switch_backend('TkAgg')

    plt.figure(figsize=(10, 6))
    sns.barplot(x=dish_frequencies, y=dish_names, palette="viridis")
    plt.title("Most Ordered Dishes")
    plt.xlabel("Number of Orders")
    plt.ylabel("Dishes")
    plt.tight_layout()

    plt.show(block=True)