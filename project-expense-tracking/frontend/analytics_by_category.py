import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"


def analytics_category_tab():
    # Set solid background color for the whole app
    background_color = "#1a1a1d"  # Dark background color
    text_color = "#ff204e"  # Bright text color for dark background
    input_background_color = "#333333"  # Dark grey background for input fields

    # Apply custom CSS for background and to remove white boxes
    st.markdown(
        f"""
        <style>
        body {{
            background-color: {background_color};
            color: {text_color};
        }}
        .streamlit-expanderHeader {{
            color: {text_color};
        }}
        .css-1kyxreq {{
            background-color: {background_color} !important;
            border: none !important;
        }}
        .css-ffhzg2 {{
            background-color: {background_color} !important;
            border: none !important;
        }}
        .css-1v3fvcr {{
            background-color: {background_color} !important;
            border: none !important;
        }}
        .stMetric, .stTable {{
            background-color: {background_color} !important;
            color: {text_color} !important;
        }}
        .css-1h8nd6e {{
            background-color: {background_color} !important;
        }}

        /* Style for date input fields */
        .stDateInput input {{
            background-color: {input_background_color} !important;
            color: #ffffff !important; /* White text */
            border: 1px solid {input_background_color} !important;
        }}
        .stDateInput label {{
            color: {text_color} !important;
        }}
        </style>
        """, unsafe_allow_html=True)

    # Create a container for date inputs
    with st.container():
        st.markdown(f"<p style='color: {text_color}; margin-bottom: 1rem;'>Select date range for analysis</p>",
                    unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                datetime(2024, 8, 1),
                help="Select the start date for analysis"
            )

        with col2:
            end_date = st.date_input(
                "End Date",
                datetime(2024, 8, 5),
                help="Select the end date for analysis"
            )

    # Analysis button with custom styling
    analyze_button = st.button(
        "Analyze Expenses",
        help="Click to analyze expenses for the selected date range",
        use_container_width=True
    )

    if analyze_button:
        try:
            with st.spinner("Analyzing expenses..."):
                payload = {
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d")
                }

                response = requests.post(f"{API_URL}/analytics/", json=payload)
                response.raise_for_status()
                data = response.json()

                # Extract data from the "breakdown" structure
                breakdown_data = data["breakdown"]

                # Create DataFrame from the breakdown data
                df = pd.DataFrame([{
                    "Category": category,
                    "Total": category_data["total"],
                    "Percentage": category_data["percentage"]
                }
                    for category, category_data in breakdown_data.items()])

                df_sorted = df.sort_values(by="Percentage", ascending=False)

                # Display total in a metric card
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        "Total Expenses",
                        f"${data['total']:,.2f}",
                        help="Total expenses for the selected period"
                    )
                with col2:
                    st.metric(
                        "Highest Category",
                        df_sorted.iloc[0]["Category"],
                        f"${float(df_sorted.iloc[0]['Total']):,.2f}"
                    )
                with col3:
                    st.metric(
                        "Categories",
                        len(df_sorted),
                        help="Number of expense categories"
                    )

                # Create enhanced bar chart
                fig = px.bar(
                    df_sorted,
                    x="Category",
                    y="Percentage",
                    title="Expense Distribution by Category",
                    text="Percentage",
                    color="Category",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )

                fig.update_traces(
                    texttemplate='%{text:.1f}%',
                    textposition='outside',
                    hovertemplate='<b>%{x}</b><br>Percentage: %{y:.1f}%<extra></extra>'
                )

                fig.update_layout(
                    xaxis_title="Category",
                    yaxis_title="Percentage (%)",
                    showlegend=False,
                    plot_bgcolor=background_color,
                    height=500,
                    title_x=0.5,
                    title_font_size=20
                )

                st.plotly_chart(fig, use_container_width=True)

                # Format and display detailed table
                st.markdown("### Detailed Breakdown")
                df_display = df_sorted.copy()
                df_display["Total"] = df_display["Total"].apply(lambda x: f"${x:,.2f}")
                df_display["Percentage"] = df_display["Percentage"].apply(lambda x: f"{x:.1f}%")
                st.table(df_display)

        except requests.exceptions.RequestException as e:
            st.error(f"⚠️ Failed to fetch analytics data: {str(e)}")
        except Exception as e:
            st.error(f"⚠️ An error occurred while processing the data: {str(e)}")
            if st.checkbox("Show debug information"):
                st.write("Response data structure:", data)
