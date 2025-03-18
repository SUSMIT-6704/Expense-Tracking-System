import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"


def analytics_months_tab():
    try:
        with st.spinner("Loading monthly data..."):
            response = requests.get(f"{API_URL}/monthly_summary/")
            response.raise_for_status()
            monthly_summary = response.json()

            df = pd.DataFrame(monthly_summary)
            df.rename(columns={
                "expense_month": "Month Number",
                "month_name": "Month Name",
                "total": "Total"
            }, inplace=True)
            df_sorted = df.sort_values(by="Month Number", ascending=False)
            df_sorted.set_index("Month Number", inplace=True)

            # Display summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Total Monthly Expenses",
                    f"${df_sorted['Total'].sum():,.2f}",
                    help="Sum of all monthly expenses"
                )
            with col2:
                st.metric(
                    "Average Monthly Expense",
                    f"${df_sorted['Total'].mean():,.2f}",
                    help="Average expense per month"
                )
            with col3:
                st.metric(
                    "Highest Monthly Expense",
                    f"${df_sorted['Total'].max():,.2f}",
                    help="Highest single month expense"
                )

            # Enhanced bar chart
            fig = px.bar(
                df_sorted.reset_index(),
                x="Month Name",
                y="Total",
                color="Total",
                color_continuous_scale="Viridis",
                title="Monthly Expense Distribution",
                labels={"Total": "Expenses ($)", "Month Name": "Month"}
            )

            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Total: $%{y:,.2f}<extra></extra>"
            )

            fig.update_layout(
                plot_bgcolor='white',
                height=500,
                title_x=0.5,
                title_font_size=20,
                showlegend=False,
                coloraxis_showscale=False
            )

            st.plotly_chart(fig, use_container_width=True)

            # Show trend analysis
            st.markdown("### Monthly Trend Analysis")
            df_sorted['MoM Change'] = df_sorted['Total'].pct_change() * 100
            df_sorted['3-Month Avg'] = df_sorted['Total'].rolling(3).mean()

            # Create analysis table
            analysis_df = df_sorted.copy()
            analysis_df['Total'] = analysis_df['Total'].apply(lambda x: f"${x:,.2f}")
            analysis_df['MoM Change'] = analysis_df['MoM Change'].apply(
                lambda x: f"{x:+.1f}%" if pd.notnull(x) else "N/A")
            analysis_df['3-Month Avg'] = analysis_df['3-Month Avg'].apply(
                lambda x: f"${x:,.2f}" if pd.notnull(x) else "N/A")

            # Style the table
            styled_df = pd.DataFrame({
                'Month': analysis_df.index,
                'Month Name': analysis_df['Month Name'],
                'Total Expenses': analysis_df['Total'],
                'Month-over-Month Change': analysis_df['MoM Change'],
                'Three Month Average': analysis_df['3-Month Avg']
            })

            st.table(styled_df)

    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Failed to fetch monthly summary: {str(e)}")
    except Exception as e:
        st.error(f"⚠️ An error occurred: {str(e)}")
        if st.checkbox("Show debug information"):
            st.write("Error details:", str(e))


if __name__ == "__main__":
    st.set_page_config(page_title="Monthly Analytics", layout="wide")
    analytics_months_tab()