from fonctions.visualization import display_graph_image
from pathlib import Path

graph_image_path = Path("docs/dish_occurrences.png")

print("start test")
display_graph_image(graph_image_path)
print("end of test.")
