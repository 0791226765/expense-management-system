import streamlit as st
from add_update_ui import add_update_tab
from analytics_ui import category_analytics_tab
from analytics_ui import monthly_analytics_tab
from trend_analysis_ui import daily_analytics_tab
st.title("Expense Management System")
tab1,tab2,tab3 = st.tabs(["Add/Update","Summary Analysis","Trend Analyis"])

with tab1:
    add_update_tab()
with tab2:
    category_analytics_tab()
    monthly_analytics_tab()
with tab3:
    daily_analytics_tab()

