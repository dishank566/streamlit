import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

from dateutil.relativedelta import relativedelta
from plotly.subplots import make_subplots
from google.cloud.bigquery.client import Client

from src.charts.tile import header_left
# from src.charts.charts import horizontal_bar_chart_with_value, trend_comparison_line_chart, trend_comparison_line_chart_aov, grouped_bar_chart_with_line_chart_2, bar_chart_with_line_chart, pie_chart, pie_chart_2, grouped_bar_chart, grouped_bar_chart_groupby, get_trendline_charts
# from config import *
from src.tabs.tab1 import tab__1
from src.tabs.tab2 import tab__2
from src.tabs.tab3 import tab__3
from src.tabs.tab4 import tab__4
from src.tabs.tab5 import tab__5
from src.tabs.tab6 import tab__6
from src.tabs.tab7 import tab__7
# from src.tabs.tab8 import tab__8

# table_names  = ['mts_recency_buckets', 'mts_aov_quartiles',
#                 'mts_daily_repeat_order_intervals',
#                 'mts_customer_retention_by_first_order_categories',
#                 'mts_customer_profile_by_product', 'mts_revenue_retention_cohorts',
#                 'mts_customer_retention_by_city_absolute',
#                 'mts_daily_repeating_customers_rate',
#                 'mts_customer_retention_by_city_percentage',
#                 'mts_customer_retention_by_channel_absolute',
#                 'mts_customer_retention_by_channel_percentage',
#                 'mts_acquisition_month_frequency_bucket_counts',
#                 'mts_order_count_at_n_order', 'mts_daily_cv_by_acquisition_date',
#                 'mts_customer_average_monthly_revenue',
#                 'mts_daily_orders_customers_sales_revenue',
#                 'mts_avg_cv_by_marketing_channel', 'mts_daily_aov_at_n_order',
#                 'mts_frequency_buckets',
#                 'mts_customer_profile_by_channel',
#                 'mts_total_discounted_orders',
#                 'mts_city_level_cv90',
#                 'mts_cohort_one_kpi_perc',
#                 'mts_cv_daily']

tab_1 = ['mts_daily_orders_customers_sales_revenue','mts_recency_buckets', 'mts_frequency_buckets', 'mts_aov_quartiles']
tab_2 = ['mts_cv_daily', 'mts_avg_cv_by_marketing_channel']
tab_3 = ['mts_daily_repeat_order_intervals', 'mts_daily_repeating_customers_rate', 'mts_daily_aov_at_n_order', 'mts_acquisition_month_frequency_bucket_counts']
tab_4 = ['mts_customer_profile_by_channel', 'mts_customer_profile_by_product']
tab_5 = ['mts_customer_profile_by_channel', 'mts_city_level_cv90']
tab_6 = ['mts_cohort_one_kpi_perc']
tab_7 = ['mts_customer_retention_by_city_absolute', 'mts_customer_retention_by_city_percentage', 'mts_customer_retention_by_channel_absolute', 'mts_customer_retention_by_channel_percentage']
# tab_8 = ['mts_recency_buckets', 'mts_frequency_buckets', 'mts_aov_quartiles']
table_names = tab_1 + tab_2 + tab_3 + tab_4 + tab_5 + tab_6 + tab_7 

@st.cache_data
def date_change_timedelta(string_1): # convert date string to timedelta
    return datetime.datetime.strptime(string_1, "%Y-%m-%d").date()


@st.cache_data
def previous_time_delta_percentage(dataframe,
                                   date_today,
                                   option, 
                                   custom_date_start=datetime.datetime(2023,2,1), 
                                   custom_date_end=datetime.datetime(2023,6,1), date_var= 'OrderDate'):
    
    if option == 'All Data':
        return dataframe, pd.DataFrame()
    
    else:
        option_dict = {'This Month': relativedelta(months=1), 'This Quarter': relativedelta(months=3), 'This Year':relativedelta(months=12), 'Last 7 Days': pd.Timedelta(days=6), 'Last 30 Days': pd.Timedelta(days=29), 'Custom Range': custom_date_end - custom_date_start}
        option_dict_start_date = {'This Month': date_today.replace(day=1), 'This Quarter': date_today - pd.DateOffset(months=(date_today.month - 1) % 3, days=date_today.day - 1), 'This Year': date_today.replace(day=1, month=1), 'Last 7 Days': date_today - pd.Timedelta(days=7), 'Last 30 Days': date_today - pd.Timedelta(days=30), 'Custom Range': pd.Timestamp(custom_date_start)}
        start_date = option_dict_start_date[option]
        dataframe_ = dataframe[(dataframe[date_var] >= start_date) & (dataframe[date_var] <= date_today)]
        delta_start_date = start_date - option_dict[option]
        delta_end_date = date_today - option_dict[option]
        dataframe_delta = dataframe[(dataframe[date_var] >= delta_start_date) & (dataframe[date_var] <= delta_end_date)]
        return dataframe_, dataframe_delta
    
def previous_time(date_today, option, custom_date_start=datetime.datetime(2023,2,1), custom_date_end=datetime.datetime(2023,6,1)):

    option_dict = {'This Month': relativedelta(months=1), 'This Quarter': relativedelta(months=3), 'This Year':relativedelta(months=12), 'Last 7 Days': pd.Timedelta(days=6), 'Last 30 Days': pd.Timedelta(days=29), 'Custom Range': custom_date_end - custom_date_start}
    option_dict_start_date = {'This Month': date_today.replace(day=1), 'This Quarter': date_today - pd.DateOffset(months=(date_today.month - 1) % 3, days=date_today.day - 1), 'This Year': date_today.replace(day=1, month=1), 'Last 7 Days': date_today - pd.Timedelta(days=7), 'Last 30 Days': date_today - pd.Timedelta(days=30), 'Custom Range': pd.Timestamp(custom_date_start)}
    if option != 'All Data':
        start_date = option_dict_start_date[option]
        # dataframe_ = dataframe[(dataframe['OrderDate'] >= start_date) & (dataframe['OrderDate'] <= date_today)]
        delta_start_date = start_date - option_dict[option]
        delta_end_date = date_today - option_dict[option]
        # dataframe_delta = dataframe[(dataframe['OrderDate'] > delta_start_date) & (dataframe['OrderDate'] <= delta_end_date)]
        return start_date, date_today, delta_start_date, delta_end_date
    else:
        return datetime.datetime(1900,1,1), date_today, datetime.datetime(1900,1,1), datetime.datetime(1901,1,1)

if __name__ == "__main__":
    
    st.set_page_config(layout="wide", page_title="E-commerce Dashboard")
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # # read mart tables
    table_dict = {table_name: pd.read_csv(f'src/data_3/{table_name}.csv') for table_name in table_names}

    table_dict['mts_daily_orders_customers_sales_revenue']['AOV'] = (table_dict['mts_daily_orders_customers_sales_revenue']['Revenue']
                                                                     /table_dict['mts_daily_orders_customers_sales_revenue']['Total_Orders'])
    
    table_dict['mts_daily_orders_customers_sales_revenue'] = table_dict['mts_daily_orders_customers_sales_revenue'].assign(OrderDate = lambda x: pd.to_datetime(x['OrderDate']))
    table_dict['mts_daily_repeating_customers_rate'] = table_dict['mts_daily_repeating_customers_rate'].assign(OrderDate = lambda x: pd.to_datetime(x['OrderDate']))
    
    
    # date_today = datetime.datetime.now().date()
    date_today = datetime.datetime(2024, 3, 6)


    
    
    # Streamlit dashboard layout
    col1, col2 = st.columns([3, 1])    

    with col1:

        header_left('E-Commerce Executive Dashboard', 44)

    listTabs = ['Executive Summary', 'Customer value cohort', 
                'Customer retention by first source', 
                'Best Customer profile','Worst cohorts', 'Cohort Analysis', 
                'Cohort Analysis 2']
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([s.center(18,"\u2001") for s in listTabs])

    with tab1: 
        col1, col2 = st.columns([3, 1])    

        with col2:

            option = st.selectbox('',
                ('This Month', 'This Quarter', 'This Year', 'Last 7 Days', 'Last 30 Days', 'All Data', 'Custom Range'))
            
        if option == 'Custom Range':
            col_1,col_2,col_3, col_4 = st.columns(4)
            with col_3:
                date_start = st.date_input("Start Date", datetime.date(2022, 7, 6))
            with col_4:
                date_end = st.date_input("End Date", datetime.date(2023, 7, 6))
                tab_1,tab_1_delta = previous_time_delta_percentage(dataframe=table_dict['mts_daily_orders_customers_sales_revenue'], 
                                                                date_today=date_today, 
                                                                option=option,
                                                                custom_date_start=date_start,
                                                                custom_date_end=date_end, date_var='OrderDate')
        else:
            tab_1,tab_1_delta = previous_time_delta_percentage(dataframe=table_dict['mts_daily_orders_customers_sales_revenue'],
                                                                                date_today=date_today,
                                                                                option=option, date_var='OrderDate')
            
        total_revenue = tab_1['Revenue'].sum()
        total_orders = tab_1['Total_Orders'].sum()
        aov = total_revenue / total_orders 
        new_customers = tab_1['Total_New_Customers'].sum()
        repeat_customers = tab_1['Total_Repeat_Customers'].sum()
        total_discounted_orders = tab_1['TotalDiscountedOrders'].sum()
        
        new_customers_delta = tab_1_delta['Total_New_Customers'].sum()
        repeat_customers_delta = tab_1_delta['Total_Repeat_Customers'].sum()
        total_orders_delta = tab_1_delta['Total_Orders'].sum()
        total_revenue_delta = tab_1_delta['Revenue'].sum()
        aov_delta = total_revenue_delta / total_orders_delta 
        total_discounted_orders_delta = tab_1_delta['TotalDiscountedOrders'].sum()

        tab__1(table_dict,total_revenue, total_revenue_delta, total_orders, total_orders_delta, aov, aov_delta, new_customers, new_customers_delta, repeat_customers, repeat_customers_delta, total_discounted_orders, total_discounted_orders_delta,option,tab_1, tab_1_delta)
        
        
    with tab2:
        col1, col2 = st.columns([3, 1])    

        with col2:

            option = st.selectbox('',
                ('This Year', 'This Quarter','All Data', 'Custom Range'), key='tab_2')
            
        if option == 'Custom Range':
            col_1,col_2,col_3, col_4 = st.columns(4)
            with col_3:
                date_start = st.date_input("Start Date", datetime.date(2022, 7, 6))
            with col_4:
                date_end = st.date_input("End Date", datetime.date(2023, 7, 6))
        
            st_date,_,_,_ = previous_time(date_today,option,date_start,date_end)
        else:
            st_date,_,_,_ = previous_time(date_today,option)
        
        tab__2(table_dict, option, st_date)

    with tab3:
        col1, col2 = st.columns([3, 1])   
        data = table_dict['mts_daily_repeat_order_intervals']
        data['FirstOrderDate'] = pd.to_datetime(data['FirstOrderDate']) 

        with col2:

            option = st.selectbox('',
                ('This Month', 'This Quarter', 'This Year', 'Last 7 Days', 'Last 30 Days', 'All Data', 'Custom Range'), key='tab_3')
            
        if option == 'Custom Range':
            col_1,col_2,col_3, col_4 = st.columns(4)
            with col_3:
                date_start = st.date_input("Start Date", datetime.date(2022, 7, 6))
            with col_4:
                date_end = st.date_input("End Date", datetime.date(2023, 7, 6))
            st_date,_,_,_ = previous_time(date_today,option,date_start,date_end)
            tab_3,tab_3_delta = previous_time_delta_percentage(dataframe=data, 
                                                                date_today=date_today, 
                                                                option=option,
                                                                custom_date_start=date_start,
                                                                custom_date_end=date_end, date_var='FirstOrderDate')
        else:
            st_date,_,_,_ = previous_time(date_today,option)
            tab_3,tab_3_delta = previous_time_delta_percentage(dataframe=data,
                                                                date_today=date_today,
                                                                option=option, date_var='FirstOrderDate')


        tab__3(table_dict,option, st_date,date_today, tab_3, tab_3_delta)
    
    with tab4:
        tab__4(table_dict)

    with tab5:
        tab__5(table_dict,option)

    with tab6:
        col1, col2 = st.columns([3, 1])    

        with col2:

            option = st.selectbox('',
                ('This Year', 'This Quarter', 'All Data', 'Custom Range'), key='tab_6')
            
        if option == 'Custom Range':
            col_1,col_2,col_3, col_4 = st.columns(4)
            with col_3:
                date_start = st.date_input("Start Date", datetime.date(2022, 7, 6))
            with col_4:
                date_end = st.date_input("End Date", datetime.date(2023, 7, 6))
        
            st_date,_,_,_ = previous_time(date_today,option,date_start,date_end)
        else:
            st_date,_,_,_ = previous_time(date_today,option)

        tab__6(table_dict, option, st_date, )

    with tab7:
        tab__7(table_dict)

    # with tab8:
    #     tab__8(table_dict)