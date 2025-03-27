import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import altair as alt

API_URL = "https://expense-management-system-aufr.onrender.com"

def daily_analytics_tab():
    # User selects the month and year for daily analytics
    col1, col2 = st.columns(2)
    with col1:
        month = st.selectbox("Select Month", [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
    with col2:
        year = st.number_input("Select Year", min_value=2000, max_value=2100, value=datetime.today().year, step=1, key="daily_year_input")

    # Initialize session state for analytics data & view selection
    if "daily_analytics_data" not in st.session_state:
        st.session_state["daily_analytics_data"] = None  # Store API data in session state

    # Define valid view options
    options = ["Show Trend", "Table"]
    # Set default value if missing or invalid
    if "daily_selected_view" not in st.session_state or st.session_state["daily_selected_view"] not in options:
        st.session_state["daily_selected_view"] = "Show Trend"

    # Fetch analytics data when button is clicked
    if st.button("Get Daily Analytics"):
        payload = {"month": month, "year": year}
        response = requests.post(f"{API_URL}/analytics/daily/", json=payload)

        if response.status_code == 200:
            response_data = response.json()
            data = {
                "Day": list(response_data.keys()),  # Extracting day numbers
                "Total": [response_data[day]["total"] for day in response_data]
            }
            st.session_state["daily_analytics_data"] = pd.DataFrame(data)
        else:
            st.error("Failed to retrieve daily expense summary.")

    # Only display analytics if data exists
    if st.session_state["daily_analytics_data"] is not None:
        df_sorted = st.session_state["daily_analytics_data"].sort_values(by="Day", ascending=True)

        # Dynamic Title with Reduced Size
        st.markdown(
            f"<h3 style='text-align: left; font-size:24px; font-weight:bold;'>Daily Expenditure for {month} {year}</h3>",
            unsafe_allow_html=True
        )

        # Arrange radio buttons horizontally and remove header text
        view_option = st.radio(
            "select",  # This label is hidden because label_visibility is "collapsed"
            options,
            index=options.index(st.session_state["daily_selected_view"]),
            horizontal=True,
            label_visibility="collapsed",
            key="daily_view_radio"
        )

        # Update session state with the current selection
        st.session_state["daily_selected_view"] = view_option

        if view_option == "Show Trend":
            # Create Area Chart with Customizations
            chart = (
                alt.Chart(df_sorted)
                .mark_area(color="darkblue", opacity=0.5)  # Area Chart with transparency
                .encode(
                    x=alt.X("Day:O", title="Days of the Month",
                            axis=alt.Axis(labelColor="black", titleFontWeight="bold", grid=False)),
                    y=alt.Y("Total:Q", title="Total Expenditure",
                            axis=alt.Axis(titleFontWeight="bold", titleColor="black", grid=False)),
                    tooltip=["Day", alt.Tooltip("Total:Q", format=",.2f")]
                )
            )

            # Create Data Labels
            text_labels = (
                alt.Chart(df_sorted)
                .mark_text(align="center", dy=-10, fontSize=12, color="black")  # Adjust dy to position labels
                .encode(
                    x="Day:O",
                    y="Total:Q",
                    text=alt.Text("Total:Q", format=",.2f")  # Format numbers with commas
                )
            )

            # Combine Area Chart and Labels
            final_chart = chart + text_labels

            # Display in Streamlit
            st.altair_chart(final_chart, use_container_width=True)

        else:
            # Ensure index starts from 1 and is displayed as a column
            df_sorted = df_sorted.reset_index(drop=True)  # Reset original index
            df_sorted.index = df_sorted.index + 1  # Set index to start from 1
            df_sorted.index.name = "S/N"  # Rename index column

            # Format Table Data for Display
            df_sorted["Total"] = df_sorted["Total"].map("{:,.2f}".format)  # Formatting with commas

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
