import streamlit as st

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f9fafb;
        font-family: Arial, sans-serif;
    }
    .main-title {
        font-size: 3em;
        color: #1b4965;
        text-align: center;
        margin-bottom: 20px;
    }
    .subtitle {
        font-size: 1.5em;
        color: #5a5a5a;
        text-align: center;
        margin-bottom: 40px;
    }
    .button-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 50px;
    }
    .dashboard-button {
        background-color: #eef2f3;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        width: 250px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease, transform 0.2s ease;
        cursor: pointer;
    }
    .dashboard-button:hover {
        background-color: #d9e4ea;
        transform: scale(1.05);
    }
    .dashboard-title {
        font-size: 1.5em;
        color: #1b4965;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .dashboard-description {
        font-size: 1em;
        color: #5a5a5a;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        color: #5a5a5a;
        font-size: 0.9em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Homepage layout
st.markdown("<div class='main-title'>🌍 Environmental Data Hub</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Explore insights into water resources, air quality, and their interconnections.</div>",
    unsafe_allow_html=True,
)

# Dashboard buttons with consistent styling
st.markdown(
    """
    <div class='button-container'>
        <div class='dashboard-button' onclick="window.location.href='/appwater'">
            <div class='dashboard-title'>🌊 Water Resource Dashboard</div>
            <div class='dashboard-description'>Insights into New Mexico's water resources, including snow depth and groundwater trends.</div>
        </div>
        <div class='dashboard-button' onclick="window.location.href='/app'">
            <div class='dashboard-title'>🌫️ Air Quality Viewer</div>
            <div class='dashboard-description'>Overview of air quality data for New Mexico, including trends in AQI (Air Quality Index).</div>
        </div>
        <div class='dashboard-button' onclick="window.location.href='/correlation'">
            <div class='dashboard-title'>🔗 Correlation Dashboard</div>
            <div class='dashboard-description'>Displays correlations between various environmental factors, highlighting interdependencies in New Mexico.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Disclaimer about navigation
st.markdown(
    """
    **Note:** The back buttons on each of the dashboards currently do not work as intended. Please use the sidebar to navigate between different sections of the site. 
    The sidebar can be accessed by clicking the arrow at the top-left of the screen. You can return here anytime to choose a different dashboard.
    """
)

# Footer
unique_names = ["Sumo Alexandre", "Ariel Arrellin", "Ryan Garcia", "Timothy Saucier", "Mitchell Snyder", "Christian Talamantes"]
footer_text = "Made with ❤️ by " + " | ".join(unique_names) + " | Powered by Streamlit"

st.markdown(
    f"""
    <div class='footer'>
        {footer_text}
    </div>
    """,
    unsafe_allow_html=True,
)
