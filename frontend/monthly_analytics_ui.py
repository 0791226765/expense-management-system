import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import altair as alt

API_URL = "https://expense-management-system-aufr.onrender.com"
def monthly_analytics_tab():
    # User selects the year for analytics
    year = st.number_input("Select Year", min_value=2000, max_value=2100, value=datetime.today().year, step=1,key="monthly_year_input")

    # Initialize session state for analytics data & view selection
    if "monthly_analytics_data" not in st.session_state:
        st.session_state["monthly_analytics_data"] = None  # Store API data in session state
    if "monthly_selected_view" not in st.session_state:
        st.session_state["monthly_selected_view"] = "Bar Chart"  # Store selected view in session state

    # Fetch analytics data when button is clicked
    if st.button("Get Monthly Analytics"):
        payload = {"year": year}
        response = requests.post(f"{API_URL}/analytics/monthly/", json=payload)

        if response.status_code == 200:
            response_data = response.json()
            data = {
                "Month": list(response_data.keys()),
                "Total": [response_data[month]["total"] for month in response_data],
                "Percentage": [response_data[month]["percentage"] for month in response_data]
            }
            st.session_state["monthly_analytics_data"] = pd.DataFrame(data)
        else:
            st.error("Failed to retrieve monthly expense summary.")

    # Only display analytics if data exists
    if st.session_state["monthly_analytics_data"] is not None:
        df_sorted = st.session_state["monthly_analytics_data"].sort_values(by="Total", ascending=False)

        # Dynamic Title with Reduced Size
        st.markdown(
            f"<h3 style='text-align: left; font-size:24px; font-weight:bold;'>Monthly Expenditure for {year}</h3>",
            unsafe_allow_html=True
        )

        # Arrange radio buttons horizontally and remove header
        view_option = st.radio(
            "Select View",
            ["Bar Chart", "Table"],
            index=["Bar Chart", "Table"].index(st.session_state["monthly_selected_view"]),
            horizontal=True,
            label_visibility="collapsed",
            key="monthly_view_radio"
        )

        # Store the selected view in session state
        st.session_state["monthly_selected_view"] = view_option

        if view_option == "Bar Chart":
            # Create Vertical Bar Chart with Customizations
            chart = (
                alt.Chart(df_sorted)
                .mark_bar(color="darkblue")  # Blue bars
                .encode(
                    x=alt.X("Month:N",
                            axis=alt.Axis(labelAngle=0, labelColor="black",labelFontWeight="bold", title = None)), # X-axis labels horizontal
                    y=alt.Y("Total:Q",
                            axis=alt.Axis(labelColor="black",title="Total Expenditure", titleFontWeight="bold", titleColor="black", grid=False)),
                    # Y-axis title bold black & grid lines removed
                    tooltip=["Month", alt.Tooltip("Total:Q", format=",.2f")]  # Rounded percentages in tooltip
                )
            )

            # Add Data Labels (Rounded to 2 Decimal Places)
            text = (
                alt.Chart(df_sorted)
                .mark_text(dy=-10, color="black", fontWeight="bold")  # Labels positioned above bars & bold black
                .encode(
                    x="Month:N",
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
            df_sorted["Total"] = df_sorted["Total"].map("{:,.2f}".format)  # ✅ Formatting with commas
            df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}".format)  # ✅ Rounded to 2 decimal places

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
