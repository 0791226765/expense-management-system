import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import altair as alt

API_URL = "https://expense-management-system-aufr.onrender.com"


def category_analytics_tab():
    col1, col2 = st.columns(2)
    today = datetime.today().date() # Today's date
    first_day = today.replace(day=1) # First day of the current month
    with col1:
        start_date = st.date_input("Start Date", first_day)
    with col2:
        end_date = st.date_input("End Date", today)

    # Extract month and year dynamically
    month_year = start_date.strftime("%B %Y") if start_date.month == end_date.month and start_date.year == end_date.year \
        else f"{start_date.strftime('%B %Y')} - {end_date.strftime('%B %Y')}"

    # Initialize session state for analytics data & view selection
    if "analytics_data" not in st.session_state:
        st.session_state["analytics_data"] = None  # Store API data in session state
    if "selected_view" not in st.session_state:
        st.session_state["selected_view"] = "Bar Chart"  # Store selected view in session state

    # Fetch analytics data when button is clicked
    if st.button("Get Category Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        response = requests.post(f"{API_URL}/analytics", json=payload)
        response = response.json()

        # Store API response in session state
        data = {
            "Category": list(response.keys()),
            "Total": [response[category]["total"] for category in response],
            "Percentage": [response[category]["percentage"] for category in response]
        }
        st.session_state["analytics_data"] = pd.DataFrame(data)

    # Only display analytics if data exists
    if st.session_state["analytics_data"] is not None:
        df_sorted = st.session_state["analytics_data"].sort_values(by="Total", ascending=False)

        # Dynamic Title with Reduced Size
        st.markdown(
            f"<h3 style='text-align: left; font-size:24px; font-weight:bold;'>Expenditure by Category for {month_year}</h3>",
            unsafe_allow_html=True)

        # Arrange radio buttons horizontally and remove header
        view_option = st.radio(
            "select view",
            ["Bar Chart", "Table"],
            index=["Bar Chart", "Table"].index(st.session_state["selected_view"]),
            horizontal=True,
            label_visibility="collapsed",
            key="category_view_radio"
        )

        # Store the selected view in session state
        st.session_state["selected_view"] = view_option

        if view_option == "Bar Chart":
            # Create Vertical Bar Chart with Customizations
            chart = (
                alt.Chart(df_sorted)
                .mark_bar(color="darkblue")  # Blue bars
                .encode(
                    x=alt.X("Category:N",
                            axis=alt.Axis(labelAngle=0, labelColor="black", title="Category", titleFontWeight="bold",
                                          titleColor="black")),  # X-axis labels horizontal & title bold black
                    y=alt.Y("Total:Q",
                            axis=alt.Axis(title="Total Expenditure", titleFontWeight="bold", titleColor="black", grid=False)),
                    # Y-axis title bold black & grid lines removed
                    tooltip=["Category", alt.Tooltip("Total:Q", format=",.2f")]  # Rounded percentages in tooltip
                )
            )

            # Add Data Labels (Rounded to 2 Decimal Places)
            text = (
                alt.Chart(df_sorted)
                .mark_text(dy=-10, color="black", fontWeight="bold")  # Labels positioned above bars & bold black
                .encode(
                    x="Category:N",
                    y="Total:Q",
                    text=alt.Text("Total:Q", format=",.2f")  # Rounded to 2 decimal places
                )
            )

            # Combine Bar Chart and Data Labels
            final_chart = chart + text

            # Display Chart in Streamlit
            st.altair_chart(final_chart, use_container_width=True)

        else:
            # Ensure index starts from 1 and is displayed as a column
            df_sorted = df_sorted.reset_index(drop=True)  # Reset original index
            df_sorted.index = df_sorted.index + 1  # Set index to start from 1
            df_sorted.index.name = "S/N"  # Rename index column

            # Format Table Data for Display
            df_sorted["Total"] = df_sorted["Total"].map("{:,.2f}".format)  # Formatting with commas
            df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)  # Rounded to 2 decimal places

            # Apply custom table styling
            st.markdown(
                """
                <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                thead th {
                    background-color: darkblue !important;
                    color: white !important;
                    font-weight: bold !important;
                    text-align: left !important;
                    padding: 10px !important;
                }
                tbody td {
                    text-align: left !important;
                    padding: 8px !important;
                }
                tbody tr td:first-child {
                    font-weight: bold !important;
                    color: black !important;
                    text-align: left !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            # Display table with new styling
            st.table(df_sorted)
