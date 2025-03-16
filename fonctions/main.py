from menu import ask_meal
from allergies import ask_allergies
from recap import welcome_message, print_recap
from visualization import display_graph_image
from pathlib import Path

print(welcome_message)

if __name__ == "__main__":
    """
    Point d'entrée du programme. Demande à l'utilisateur ses allergies et propose un menu.
    Après que l'utilisateur a terminé sa commande, affiche un récapitulatif et une image de graphique.
    """
    while True:
        allergens = ask_allergies()
        ask_meal(allergens)

        # Afficher le récapitulatif de la commande
        recap_result = print_recap()
        if recap_result == "continue":
            continue  # Redémarrer le processus

        # Afficher l'image du graphique
        graph_image_path = Path("docs/dish_occurrences.png")
        display_graph_image(graph_image_path)