import pandas as pd

class MenuAnalyzer:
    """Class to analyze menu data and generate cross-tabulations."""

    def __init__(self, dishes_path, menu_path):
        """
        Initializes the class by loading datasets.
        
        Args:
            dishes_path (str): Path to the dishes dataset (CSV or Excel file).
            menu_path (str): Path to the menu dataset (CSV or Excel file).
        """
        self.dishes = pd.read_excel(dishes_path) if dishes_path.endswith(".xlsx") else pd.read_csv(dishes_path)
        self.menu = pd.read_excel(menu_path) if menu_path.endswith(".xlsx") else pd.read_csv(menu_path)

    def cross_tab_dishes_allergens(self):
        """
        Creates a cross-tabulation between dish names and their allergens.

        Returns:
            pd.DataFrame: Cross-tabulation table.
        """
        return pd.crosstab(self.dishes["dish_name"], self.dishes["product_allergen"])

    def cross_tab_meal_dish_type(self):
        """
        Creates a cross-tabulation between meal types and dish types.

        Returns:
            pd.DataFrame: Cross-tabulation table.
        """
        return pd.crosstab(self.menu["meal_type"], self.menu["dish_type"])

    def display_cross_tabs(self):
        """Prints both cross-tabulations."""
        print("\n📌 Cross-tabulation: Dishes vs. Allergens\n", self.cross_tab_dishes_allergens())
        print("\n📌 Cross-tabulation: Meal Type vs. Dish Type\n", self.cross_tab_meal_dish_type())

# Example Usage
analyzer = MenuAnalyzer("data/processed/dishes.xlsx", "data/processed/menu.xlsx")
analyzer.display_cross_tabs()
