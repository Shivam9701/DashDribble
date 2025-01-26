import streamlit as st
from utils.utils import inject_css, load_template

# Inject custom CSS
css_file = "styles/styles.css"
inject_css(css_file)

# Load HTML template
navbar_html = load_template("templates/navbar.html")
st.markdown(navbar_html, unsafe_allow_html=True)

# Content for the Home Page
st.title("Welcome to DashDribble ⚽")
st.markdown("A powerful football dashboard for leagues, teams, and players.")

# Display example table
st.write("Here is an example table of player stats:")
st.table(
    {
        "Player": ["Lionel Messi", "Cristiano Ronaldo", "Kylian Mbappé"],
        "Goals": [30, 25, 35],
        "Assists": [10, 8, 12],
    }
)
