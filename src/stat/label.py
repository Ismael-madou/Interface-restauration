from collections import Counter
from typing import Dict, List
import pandas as pd
from pathlib import Path


menu= pd.read_excel('data/processed/menu.xlsx') 


def ask_for_labels(menu: pd.DataFrame, column: str = "dish_label") -> Dict[str, int]:
    """
    Computes the frequency of each dish label in the 'menu' DataFrame.

    Args:
        menu (pd.DataFrame): The dataframe containing dish labels.
        column (str): The name of the column containing labels. Defaults to "dish_label".

    Returns:
        Dict[str, int]: A dictionary with labels as keys and their counts as values.

    Raises:
        ValueError: If the specified column does not exist in the DataFrame.
    """
    # Check if the specified column exists in the DataFrame
    if column not in menu.columns:
        raise ValueError(f"The column '{column}' does not exist in the DataFrame.")

    # Initialize a list to collect all labels
    all_labels = []

    # Iterate over each row in the specified column
    for labels in menu[column].dropna():  # Drop NaN values to avoid errors
        # Split labels by ';', strip whitespace, and convert to lowercase
        cleaned_labels = [label.strip().lower() for label in labels.split(";")]
        all_labels.extend(cleaned_labels)  # Add cleaned labels to the list

    # Count occurrences of each label using Counter
    label_counts = Counter(all_labels)

    # Return the result as a dictionary
    return dict(label_counts)

def ask_for_labels() -> Dict[str, int]:
    """
    Asks the user if they want to see the dish labels and displays the label distribution.

    Returns:
        Dict[str, int]: A dictionary with labels as keys and their counts as values.
    """
    while True:
        response = input("\nWould you like to see the distribution of dish labels? (yes/no): ").strip().lower()
        if response == "yes":
            # Compute the distribution of dish labels
            label_counts = ask_for_labels(menu, column="dish_label")

            # Display the results
            print("\nHere is the distribution of dish labels:")
            for label, count in label_counts.items():
                print(f"🍽️ {label}: {count} dishes")
            return label_counts
        elif response == "no":
            print("\nNo problem! Let me know if you change your mind.")
            return {}
        else:
            print("⚠️ Invalid response. Please enter 'yes' or 'no'.")