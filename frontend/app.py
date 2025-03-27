import streamlit as st
from add_update_ui import add_update_tab
from category_analytics_ui import category_analytics_tab
from monthly_analytics_ui import monthly_analytics_tab
from daily_analytics_ui import daily_analytics_tab
st.title("Expense Management System")
tab1, tab2, tab3, tab4 = st.tabs(["Add/Update", "Category Analytics", "Monthly Analytics", "Daily Analytics"])

with tab1:
    add_update_tab()
with tab2:
    category_analytics_tab()
with tab3:
    monthly_analytics_tab()
with tab4:
    daily_analytics_tab()

