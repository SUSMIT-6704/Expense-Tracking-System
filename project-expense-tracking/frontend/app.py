import streamlit as st
from add_update import add_update_tab
from analytics_by_category import analytics_category_tab
from analytics_by_months import analytics_months_tab

# Custom CSS with coordinated background and text colors
custom_css = """
<style>
    /* Base styles and colors */
    :root {
        --primary-color: #2C3E50;
        --secondary-color: #34495E;
        --accent-color: #3498DB;
        --background-light: #ECF0F1;
        --background-white: #FFFFFF;
        --text-dark: #2C3E50;
        --text-light: #FFFFFF;
        --border-color: #BDC3C7;
    }

    /* Main container styling */
    .main {
        background-color: var(--background-light);
        color: var(--text-dark);
        padding: 2rem;
    }

    /* Header styling */
    .stTitle {
        color: var(--primary-color);
        background-color: var(--background-white);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        padding: 0.5rem;
        background-color: var(--background-white);
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        color: var(--secondary-color);
        background-color: var(--background-light);
        border-radius: 5px;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color) !important;
        color: var(--text-light) !important;
    }

    /* Card styling */
    [data-testid="stMetric"] {
        background-color: var(--background-white);
        color: var(--text-dark);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Table styling */
    .stDataFrame {
        background-color: var(--background-white);
        color: var(--text-dark);
        border: 1px solid var(--border-color);
        border-radius: 10px;
    }

    .stDataFrame [data-testid="StyledDataFrameDataCell"] {
        background-color: var(--background-white);
        color: var(--text-dark);
    }

    /* Button styling */
    .stButton > button {
        background-color: var(--accent-color);
        color: var(--text-light);
        border-radius: 5px;
        padding: 0.5rem 2rem;
        border: none;
    }

    .stButton > button:hover {
        background-color: var(--primary-color);
        color: var(--text-light);
    }

    /* Input fields styling */
    .stDateInput, .stNumberInput, .stSelectbox {
        background-color: var(--background-white);
        color: var(--text-dark);
        border-radius: 5px;
        border: 1px solid var(--border-color);
    }

    /* Chart container styling */
    [data-testid="stPlotlyChart"] {
        background-color: var(--background-white);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Message styling */
    .stSuccess {
        background-color: #D5F5E3;
        color: #196F3D;
        padding: 1rem;
        border-radius: 5px;
    }

    .stError {
        background-color: #FADBD8;
        color: #943126;
        padding: 1rem;
        border-radius: 5px;
    }
</style>
"""


def main():
    # Page configuration
    st.set_page_config(
        page_title="Expense Tracker Pro",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Inject custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    # Header with custom styling
    st.markdown("""
        <div style='text-align: center; padding: 2rem; background-color: #FFFFFF; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: #2C3E50; font-size: 2.5rem;'>💰 Expense Tracker Pro</h1>
            <p style='color: #34495E; font-size: 1.1rem;'>Manage your expenses with ease</p>
        </div>
    """, unsafe_allow_html=True)

    # Create tabs with custom styling
    tab1, tab2, tab3 = st.tabs([
        "📝 Add/Update Expenses",
        "📊 Category Analytics",
        "📈 Monthly Trends"
    ])

    with tab1:
        st.markdown("""
            <div style='background-color: #FFFFFF; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                <h2 style='color: #2C3E50; font-size: 1.5rem;'>Add or Update Expenses</h2>
            </div>
        """, unsafe_allow_html=True)
        add_update_tab()

    with tab2:
        st.markdown("""
            <div style='background-color: #FFFFFF; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                <h2 style='color: #2C3E50; font-size: 1.5rem;'>Expense Categories Analysis</h2>
            </div>
        """, unsafe_allow_html=True)
        analytics_category_tab()

    with tab3:
        st.markdown("""
            <div style='background-color: #FFFFFF; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                <h2 style='color: #2C3E50; font-size: 1.5rem;'>Monthly Expense Trends</h2>
            </div>
        """, unsafe_allow_html=True)
        analytics_months_tab()

    # Footer
    st.markdown("""
        <div style='text-align: center; padding: 2rem; background-color: #FFFFFF; border-radius: 10px; margin-top: 3rem;'>
            <p style='color: #34495E;'>© 2024 Expense Tracker Pro - Track Smarter, Save Better</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()