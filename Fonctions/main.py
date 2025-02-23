from menu import ask_meal
from Fonctions.allergies import ask_allergies

if __name__ == "__main__":
    allergens = ask_allergies()
    ask_meal(allergens)