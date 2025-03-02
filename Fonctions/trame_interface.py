# trame_interface.py
from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, html
from messages import welcome_message, goodbye_message
from shared_data import chosen_products

# Initialize Trame server
server = get_server()
state = server.state

# Define app logic
def update_interface():
    """
    Update the interface based on user choices.
    """
    from menu import ask_meal
    from allergies import ask_allergies

    allergens = ask_allergies()
    ask_meal(allergens)
    state.summary = "\n".join([f"{product[1]}" for product in chosen_products])
    state.show_summary = True

def restart():
    """
    Reset the interface for a new order.
    """
    chosen_products.clear()
    state.summary = ""
    state.show_summary = False

# Build the Trame UI
with SinglePageLayout(server) as layout:
    layout.title.set("Restaurant Order System")

    with layout.content:
        # Display the welcome message
        html.Div(welcome_message(), style="margin-bottom: 20px;")

        # Button to start the order
        vuetify.VBtn("Start Order", click=update_interface)

        # Summary section
        with vuetify.VCard(v_if="show_summary", style="margin-top: 20px;"):
            vuetify.VCardTitle("Order Summary")
            vuetify.VCardText("{{ summary }}")

        # Restart or exit buttons
        with vuetify.VRow(v_if="show_summary", style="margin-top: 20px;"):
            vuetify.VCol(
                vuetify.VBtn("Restart", click=restart),
                cols=6,
            )
            vuetify.VCol(
                vuetify.VBtn("Exit", click=lambda: print(goodbye_message())),
                cols=6,
            )