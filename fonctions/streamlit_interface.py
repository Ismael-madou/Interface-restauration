# streamlit_interface.py
import streamlit as st
from messages import welcome_message, goodbye_message
from shared_data import chosen_products
from menu import ask_meal
from allergies import ask_allergies

def main():
    """
    Main function to run the Streamlit app.
    """
    st.title("Restaurant Order System")

    # Display the welcome message
    st.markdown(welcome_message())

    # Button to start the order
    if st.button("Start Order"):
        allergens = ask_allergies()
        ask_meal(allergens)

        # Display the order summary
        if chosen_products:
            st.subheader("Order Summary")
            for product in chosen_products:
                st.write(f"- {product[1]}")

        # Restart or exit buttons
        col1, col2 = st.columns(2)
        if col1.button("Restart"):
            chosen_products.clear()
            st.experimental_rerun()

        if col2.button("Exit"):
            st.markdown(goodbye_message())
            st.stop()