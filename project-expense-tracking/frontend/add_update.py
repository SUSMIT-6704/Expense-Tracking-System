import streamlit as st
from datetime import datetime
import requests

# Enhanced CSS with more modern styling
custom_css = """
<style>
    /* Form styling */
    div[data-testid="stForm"] {
        background-color: #FFFFFF;
        color: #2C3E50;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }

    /* Input fields */
    div[data-testid="stForm"] input, 
    div[data-testid="stForm"] select {
        background-color: #ECF0F1;
        color: #2C3E50;
        border: 1px solid #BDC3C7;
        border-radius: 5px;
        padding: 8px;
    }

    div[data-testid="stForm"] input:focus, 
    div[data-testid="stForm"] select:focus {
        border-color: #3498DB;
        box-shadow: 0 0 0 2px rgba(52,152,219,0.2);
    }

    /* Labels */
    div[data-testid="stForm"] label {
        color: #2C3E50;
        font-weight: 500;
    }

    /* Category headers */
    .category-header {
        background-color: #ECF0F1;
        color: #2C3E50;
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }

    /* Submit button */
    button[kind="primary"] {
        background-color: #3498DB;
        color: #FFFFFF;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 5px;
        font-weight: 500;
        width: 100%;
        margin-top: 1rem;
    }

    button[kind="primary"]:hover {
        background-color: #2C3E50;
    }

    /* Total amount display */
    .total-amount {
        background-color: #ECF0F1;
        color: #2C3E50;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        font-weight: 500;
        text-align: center;
    }
</style>
"""

API_URL = "http://localhost:8000"


def add_update_tab():
    st.markdown(custom_css, unsafe_allow_html=True)

    # Date selection with calendar
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_date = st.date_input(
            "Select Date",
            datetime(2024, 8, 1),
            help="Choose the date for expense entry"
        )

    # Fetch existing expenses
    try:
        with st.spinner("Loading existing expenses..."):
            response = requests.get(f"{API_URL}/expenses/{selected_date}")
            response.raise_for_status()
            existing_expenses = response.json()
    except requests.exceptions.RequestException:
        st.warning("⚠️ Could not load existing expenses. Starting with empty form.")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    # Create form with enhanced styling
    with st.form(key="expense_form"):
        st.markdown("### Enter Expenses")

        # Category headers
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<p class="category-header">Amount ($)</p>', unsafe_allow_html=True)
        with col2:
            st.markdown('<p class="category-header">Category</p>', unsafe_allow_html=True)
        with col3:
            st.markdown('<p class="category-header">Notes</p>', unsafe_allow_html=True)

        expenses = []
        total_amount = 0

        # Expense entry rows
        for i in range(5):
            amount = 0.0
            category = "Shopping"
            notes = ""

            if i < len(existing_expenses):
                amount = existing_expenses[i].get('amount', 0.0)
                category = existing_expenses[i].get("category", "Shopping")
                notes = existing_expenses[i].get("notes", "")

            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(
                    "Amount",
                    min_value=0.0,
                    step=1.0,
                    value=amount,
                    key=f"amount_{i}",
                    label_visibility="collapsed"
                )
                total_amount += amount_input

            with col2:
                category_input = st.selectbox(
                    "Category",
                    options=categories,
                    index=categories.index(category),
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )

            with col3:
                notes_input = st.text_input(
                    "Notes",
                    value=notes,
                    key=f"notes_{i}",
                    label_visibility="collapsed",
                    placeholder="Enter notes..."
                )

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        # Display total
        st.markdown(f"### Total Amount: ${total_amount:,.2f}")

        # Submit button
        submit_button = st.form_submit_button("Save Expenses", use_container_width=True)

        if submit_button:
            try:
                filtered_expenses = [exp for exp in expenses if exp['amount'] > 0]

                with st.spinner("Saving expenses..."):
                    response = requests.post(
                        f"{API_URL}/expenses/{selected_date}",
                        json=filtered_expenses
                    )
                    response.raise_for_status()

                st.success("✅ Expenses saved successfully!")

                # Show summary of saved expenses
                st.markdown("### Saved Expenses Summary")
                for expense in filtered_expenses:
                    st.markdown(f"- ${expense['amount']:,.2f} ({expense['category']}): {expense['notes']}")

            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Failed to save expenses: {str(e)}")