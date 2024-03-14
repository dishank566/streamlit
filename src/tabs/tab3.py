# Customer reetention by first source
import streamlit as st
import plotly.express as px
import pandas as pd
from src.charts.tile import kpi_tile, header, header_chart, header_left, header_pie
from src.charts.charts import horizontal_bar_chart_with_value, trend_comparison_line_chart, trend_comparison_line_chart_aov, grouped_bar_chart_with_line_chart_2, bar_chart_with_line_chart, pie_chart, pie_chart_2, grouped_bar_chart, grouped_bar_chart_groupby, get_trendline_charts


def tab__3(table_dict,option, st_date,date_today, tab_3, tab_3_delta):

    header('How well are we retaining our customers?')
    data = table_dict['mts_daily_repeat_order_intervals']
    # data = data[(data['FirstOrderDate'] > st_date) & (data['FirstOrderDate'] < date_today)]
    d2_d1, d3_d2, d4_d3 = tab_3[['D2_D1', 'D3_D2', 'D4_D3']].mean().abs()
    d2_d1_delta, d3_d2_delta, d4_d3_delta = tab_3_delta[['D2_D1', 'D3_D2', 'D4_D3']].mean().abs()
    kpi3_1,kpi3_2,kpi3_3 = st.columns(3)
    kpi_tile(kpi3_1,tile_text='Interval between 1st and 2nd Order', tile_label='', tile_value=d2_d1,option=option, delta_color_inversion = 'inverse',
                     tile_value_prefix='',delta_value=(d2_d1-d2_d1_delta)*100/d2_d1_delta,integer=True, tile_value_suffix='days', help='Average number of days between 1st and 2nd Order')
    kpi_tile(kpi3_2,tile_text='Interval between 2nd and 3rd Order', tile_label='', tile_value=d3_d2,option=option,delta_color_inversion = 'inverse',
                     tile_value_prefix='',delta_value=(d3_d2-d3_d2_delta)*100/d3_d2_delta,integer=True, tile_value_suffix='days', help='Average number of days between 2nd and 3rd Order')
    kpi_tile(kpi3_3,tile_text='Interval between 3rd and 4th Order', tile_label='', tile_value=d4_d3,option=option,delta_color_inversion = 'inverse',
                     tile_value_prefix='',delta_value=(d4_d3-d4_d3_delta)*100/d4_d3_delta,integer=True, tile_value_suffix='days', help='Average number of days between 3rd and 4th Order')
    

    header_chart('How Many Customers repeat?')
    # plot = px.bar(pivot_customer[['SecondOrderRate','ThirdOrderRate','FourthOrderRate']], barmode='group')
    # st.plotly_chart(plot, use_container_width=True)
    grouped_bar_chart(data=table_dict['mts_daily_repeating_customers_rate'].assign(Month = lambda x: pd.to_datetime(x['OrderDate']).dt.strftime('%Y-%m')), 
                      option=option,value_column_name=['SecondOrderRate','ThirdOrderRate','FourthOrderRate'],st_date=st_date,
                      index='Month', desired_order=['SecondOrderRate','ThirdOrderRate','FourthOrderRate'])
    # grouped_bar_chart(pivot_customer,option=option,value_column_name=['SecondOrderRate','ThirdOrderRate','FourthOrderRate'],index='Month', desired_order=['SecondOrderRate','ThirdOrderRate','FourthOrderRate'])


    header_chart('Average Order Value at 1st Order, 2nd Order, 3rd Order, 4th Order') 
    # plot = px.bar(Order_Attribute.pivot_table(index='Month',
    #                             columns='Order_Flag', 
    #                             values='Total_Price', 
    #                             aggfunc='mean'),
    # barmode='group'
    # )
    # st.plotly_chart(plot, use_container_width=True)  
    # grouped_bar_chart(table_dict['mts_daily_aov_at_n_order'].assign(Month = lambda x: pd.to_datetime(x['OrderDate']).dt.strftime('%Y-%m')), index='Month', value_column_name='Total_Price', option=option, column_name='Order_Flag', desired_order=['FOD_flag', 'SOD_flag','TOD_flag','FrOD_flag','Other'])
    
    # grouped_bar_chart(Order_Attribute,index='Month', value_column_name='Total_Price', option=option, column_name='Order_Flag', desired_order=['FOD_flag', 'SOD_flag','TOD_flag','FrOD_flag','Other'])
    grouped_bar_chart(data=table_dict['mts_daily_aov_at_n_order'].assign(Month = lambda x: pd.to_datetime(x['OrderDate']).dt.strftime('%Y-%m')), 
                      option=option,value_column_name=['FirstOrderRevenue','SecondOrderRevenue','ThirdOrderRevenue','FourthOrderRevenue','FourPlusOrderRevenue'],st_date=st_date,
                      index='Month', desired_order=['FirstOrderRevenue','SecondOrderRevenue','ThirdOrderRevenue','FourthOrderRevenue','FourPlusOrderRevenue'])
    

    header_chart('Repeat Order Intervals') # mts_daily_repeat_order_intervals
    # plot =px.bar(Order_Attribute.pivot_table(index='Month', 
    #                                          values=['D2_D1', 'D3_D2', 'D4_D3'], 
    #                                          aggfunc='mean').abs(),
    # barmode='group'
    # )
    # st.plotly_chart(plot, use_container_width=True)
    # grouped_bar_chart(Order_Attribute,index='Month',value_column_name=['D2_D1', 'D3_D2', 'D4_D3'],option=option, desired_order=['D2_D1', 'D3_D2', 'D4_D3'])
    grouped_bar_chart(data=table_dict['mts_daily_repeat_order_intervals'].assign(Month = lambda x: pd.to_datetime(x['FirstOrderDate']).dt.strftime('%Y-%m')), 
                      option=option,value_column_name=['D2_D1', 'D3_D2', 'D4_D3'],st_date=st_date,
                      index='Month', desired_order=['D2_D1', 'D3_D2', 'D4_D3'])
    

    header_chart('Order count at 1st Order, 2nd Order, 3rd Order, 4th Order over months')   
    # plot = px.bar(Order_Attribute.groupby('Month')['Order_Flag'].value_counts().reset_index(),
    # x='Month',
    # y='count',
    # color='Order_Flag',
    # barmode='group'
    # )
    # st.plotly_chart(plot, use_container_width=True)
    # grouped_bar_chart(Order_Attribute,index='Month',value_column_name='Order_Flag', option=option, column_name='Order_Flag_value_count', agg_func='size')
    # grouped_bar_chart_groupby(Order_Attribute,group_by='Month', index='Month',column_name='Order_Flag', option=option, desired_order=['FOD_flag', 'SOD_flag','TOD_flag','FrOD_flag','Other'])
    grouped_bar_chart(data=table_dict['mts_daily_aov_at_n_order'].assign(Month = lambda x: pd.to_datetime(x['OrderDate']).dt.strftime('%Y-%m')), 
                      option=option,value_column_name=['TotalFirstOrders','TotalSecondOrders','TotalThirdOrders','TotalFourthOrders','TotalFourPlusOrders'],st_date=st_date,
                      index='Month', desired_order=['TotalFirstOrders','TotalSecondOrders','TotalThirdOrders','TotalFourthOrders','TotalFourPlusOrders'])

    header_chart('Customer count who purchased 1 Item, 2 Items, 3 items, 3+ items')  # mts_acquisition_month_frequency_bucket_counts 
    # plot= px.bar(Order_Attribute.groupby('Month')['FrequencyBucket'].value_counts().reset_index(),
    # x='Month',
    # y='count',
    # color='FrequencyBucket',
    # barmode='group'
    # )
    # st.plotly_chart(plot, use_container_width=True)
    # grouped_bar_chart_groupby(Order_Attribute,group_by='Month', index='Month',column_name='FrequencyBucket', option=option, desired_order=['1', '2', '3', '4', '4+'])
    # grouped_bar_chart(data=table_dict['mts_acquisition_month_frequency_bucket_counts'].assign(Month = lambda x: pd.to_datetime(x['FirstOrderDate']).dt.strftime('%Y-%m')), 
    #                   option=option,value_column_name='Customer_count',column_name='FirstOrder_ItemCount',
    #                   index='Month',
    #                   desired_order=['ItemCount_1', 'ItemCount_2','ItemCount_3','ItemCount_3+']
    #                 )

    data = table_dict['mts_acquisition_month_frequency_bucket_counts'].assign(FirstOrderDate = lambda x: pd.to_datetime(x['FirstOrderDate']))
    if option == 'All Data':
        pass
    else:
        data['FirstOrderDate'] = pd.to_datetime(data['FirstOrderDate'])
        data = data[data['FirstOrderDate']>=st_date]
    # data.set_index('FirstOrderDate').groupby('FirstOrder_ItemCount')['Customer_count'].resample('M').sum().reset_index()
    
    plot = px.bar(data.set_index('FirstOrderDate').groupby('FirstOrder_ItemCount')['Customer_count'].resample('M').sum().reset_index().pivot_table(index='FirstOrderDate', 
                                columns='FirstOrder_ItemCount',
                                values='Customer_count',
                                aggfunc= 'sum'
                                ),
    
    barmode='group')

    st.plotly_chart(plot, use_container_width=True)