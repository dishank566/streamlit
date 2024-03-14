# Audience Overview
import streamlit as st
from src.charts.tile import kpi_tile, header, header_chart, header_left, header_pie
from src.charts.charts import horizontal_bar_chart_with_value, trend_comparison_line_chart, trend_comparison_line_chart_aov, grouped_bar_chart_with_line_chart_2, bar_chart_with_line_chart, pie_chart, pie_chart_2, grouped_bar_chart, grouped_bar_chart_groupby, get_trendline_charts

# mts_frequency_buckets for second pie chart pending

def tab__8(table_dict):
    # st.text('Audience Overview')
    header('Audience Overview')
    col_1,col_2,col_3 = st.columns([2,2,3])
    with col_1:
        header_pie('Audience Split by Recency Buckets')
        pie_chart(table_dict['mts_recency_buckets'],'RecencyBucket','TotalCustomers' , desired_order=['0-7', '7-15', '15-30', '30-90', '90-180', '>180'])
    with col_2:
        header_pie('Audience Split by 4 AOV quartiles')
        pie_chart(table_dict['mts_aov_quartiles'],'quartile','AOV', desired_order=[1,2,3,4])

    with col_3:
        header_pie('Audience Split by Frequency Buckets')
        col_1,col_2 = st.columns([2,1])
        with col_2:
            channel = st.selectbox('Channel',table_dict['mts_frequency_buckets']['marketing_channel'].unique(), key='tab_8_1')
            tier = st.selectbox('Tier',table_dict['mts_frequency_buckets']['Tier'].unique(), key='tab_8_2')
        with col_1:
            df = table_dict['mts_frequency_buckets'][table_dict['mts_frequency_buckets']['marketing_channel']==channel]
            df = df[df['Tier']==tier]
            pie_chart(df,'FrequencyBucket','TotalCustomers', desired_order=['0','1','2','3','4','4+']) 
    