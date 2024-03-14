# Cohort Analysis 2
import streamlit as st
from src.charts.tile import kpi_tile, header, header_chart, header_left, header_pie
from src.charts.charts import horizontal_bar_chart_with_value, trend_comparison_line_chart, trend_comparison_line_chart_aov, grouped_bar_chart_with_line_chart_2, bar_chart_with_line_chart, pie_chart, pie_chart_2, grouped_bar_chart, grouped_bar_chart_groupby, get_trendline_charts

def tab__7(table_dict):
    header('Cohort Analysis')

    # st.text('Customer Retention by City')
    header_chart('Customer Retention by City')

    data = table_dict['mts_customer_retention_by_city_absolute']
    data = data[data['month_0']>100]
    data = data.sort_values(by='month_0', ascending=False).reset_index(drop=True)
    st.dataframe(data.style.background_gradient(), use_container_width=True, hide_index=True)
    
    # st.text('Customer Percentage Retention by City')
    header_chart('Customer Percentage Retention by City')  # 
    data = table_dict['mts_customer_retention_by_city_percentage']
    data = data.sort_values(by='month_0', ascending=False).reset_index(drop=True)
    st.dataframe(data.style.background_gradient(), use_container_width=True, hide_index=True)


    # st.text('Channel-wise Cohorts')  
    header_chart('Channel-wise Cohorts')
    data = table_dict['mts_customer_retention_by_channel_absolute']
    data = data.sort_values(by='month_0', ascending=False).reset_index(drop=True)
    st.dataframe(data.style.background_gradient(), use_container_width=True, hide_index=True)



    # st.text('Channel-wise Cohorts - Customer count')
    header_chart('Channel-wise Cohorts - Customer count')
    data = table_dict['mts_customer_retention_by_channel_percentage']
    data = data.sort_values(by='month_0', ascending=False).reset_index(drop=True)
    st.dataframe(data.style.background_gradient(), use_container_width=True, hide_index=True)