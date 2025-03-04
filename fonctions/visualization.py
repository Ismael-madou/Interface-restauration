# visualization.py
import streamlit as st

def show_most_ordered_dishes_image():
    """
    Displays an image of the most ordered dishes before the user makes their selection.
    """
    image_path = "path/to/your/image.png"  # Replace with the path to your image
    st.image(image_path, caption="Most Ordered Dishes")