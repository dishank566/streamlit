# Cohort Analysis
import streamlit as st
import pandas as pd
from src.charts.tile import kpi_tile, header, header_chart, header_left, header_pie
from src.charts.charts import horizontal_bar_chart_with_value, trend_comparison_line_chart, trend_comparison_line_chart_aov, grouped_bar_chart_with_line_chart_2, bar_chart_with_line_chart, pie_chart, pie_chart_2, grouped_bar_chart, grouped_bar_chart_groupby, get_trendline_charts

def tab__6(table_dict,option,st_date):
    header('Cohort Analysis')
    header_chart('Customer Retention by First Order')
    df=table_dict['mts_cohort_one_kpi_perc'].pivot_table(index='first_purchase_month',
                   columns='month_order',
                   values='Customers').iloc[:,:9]
    df.fillna(0, inplace=True)
    df.reset_index(inplace=True)
    df['first_purchase_month'] = pd.to_datetime(df['first_purchase_month'], format="%Y%m")
    if option=='All Data':
        pass
    else:
        df = df[df['first_purchase_month']>=st_date]
    df['first_purchase_month'] = df['first_purchase_month'].dt.strftime("%b'%y")
    df.set_index('first_purchase_month', inplace=True)
    df=df.astype(int)
    
    st.dataframe(df.style.background_gradient(), use_container_width=True)
    
    header_chart('Revenue Retention Cohorts')
    df=table_dict['mts_cohort_one_kpi_perc'].pivot_table(index='first_purchase_month',
                   columns='month_order',
                   values='Revenue').iloc[:,:9]
    df.fillna(0, inplace=True)
    df.reset_index(inplace=True)
    df['first_purchase_month'] = pd.to_datetime(df['first_purchase_month'], format="%Y%m")
    if option=='All Data':
        pass
    else:
        df = df[df['first_purchase_month']>=st_date]
    df['first_purchase_month'] = df['first_purchase_month'].dt.strftime("%b'%y")
    df.set_index('first_purchase_month', inplace=True)
    df=df.astype(int)

    st.dataframe(df.style.background_gradient(), use_container_width=True)

    header_chart('Customer Average monthly Revenue') 
    df=table_dict['mts_cohort_one_kpi_perc'].pivot_table(index='first_purchase_month',
                   columns='month_order',
                   values='CustAvgMonthlyRev').iloc[:,:9]
    df.fillna(0, inplace=True)
    df.reset_index(inplace=True)
    df['first_purchase_month'] = pd.to_datetime(df['first_purchase_month'], format="%Y%m")
    if option=='All Data':
        pass
    else:
        df = df[df['first_purchase_month']>=st_date]
    df['first_purchase_month'] = df['first_purchase_month'].dt.strftime("%b'%y")
    df.set_index('first_purchase_month', inplace=True)
    df=df.astype(int)

    st.dataframe(df.style.background_gradient(), use_container_width=True)