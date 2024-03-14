# Executive summary
import streamlit as st
from src.charts.tile import kpi_tile, header, header_chart, header_left, header_pie
from src.charts.charts import horizontal_bar_chart_with_value, trend_comparison_line_chart, trend_comparison_line_chart_aov, grouped_bar_chart_with_line_chart_2, bar_chart_with_line_chart, pie_chart, pie_chart_2, grouped_bar_chart, grouped_bar_chart_groupby, get_trendline_charts

def tab__1(table_dict,total_revenue, total_revenue_delta, total_orders, total_orders_delta, aov, aov_delta, new_customers, new_customers_delta, repeat_customers, repeat_customers_delta, total_discounted_orders, total_discounted_orders_delta,option,tab_1, tab_1_delta):
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns([1.25,1,1,1,1,1]) 
    
    with st.container():
        kpi_tile(kpi1,tile_text='Revenue', tile_label='', tile_value=total_revenue, option=option,
                    tile_value_prefix='₹',delta_value=(total_revenue-total_revenue_delta)*100/total_revenue_delta,integer=True, help='Sum total of money from orders, converted into one currency')


    
        kpi_tile(kpi2,tile_text='Total Orders', tile_label='', tile_value=total_orders,option=option,
                    tile_value_prefix='',delta_value=(total_orders-total_orders_delta)*100/total_orders_delta,integer=True, help='Total Number of Orders')


    
        kpi_tile(kpi3,tile_text='Average Order Value', tile_label='', tile_value=aov,option=option,
                    tile_value_prefix='₹',delta_value=(aov-aov_delta)*100/aov_delta,integer=True, help='Average cart value of each completed order (not including returns + refunds)')


    
        kpi_tile(kpi4,tile_text='New Customers', tile_label='', tile_value=new_customers,option=option,
                    tile_value_prefix='',delta_value=(new_customers-new_customers_delta)*100/new_customers_delta,integer=True, help= 'Number of unique individuals who made first order') 


    
        kpi_tile(kpi5,tile_text="Repeat Customers", tile_label='', tile_value=repeat_customers,option=option,
                    tile_value_prefix='',delta_value=(repeat_customers-repeat_customers_delta)*100/repeat_customers_delta,integer=True,help= 'Number of unique individuals who made order more than once')

        kpi_tile(kpi6,tile_text="Discounted Orders", tile_label='', tile_value=total_discounted_orders,option=option,
                    tile_value_prefix='',delta_value=(total_discounted_orders-total_discounted_orders_delta)*100/total_discounted_orders_delta,integer=True, help= 'Count of orders that have received some form of discount')
        
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
        
    # st.text('How our key metrics are trending?')    
    header(' How our key metrics are trending?')

    # st.markdown(f'**Revenue trend & comparison with the previous period**', help = 'definition')
    header_chart('Revenue trend & comparison with the previous period')

    # st.text('Revenue trend & comparison with the previous period')   
    get_trendline_charts(df=tab_1,
                            df_delta=tab_1_delta,
                            date_col='OrderDate', 
                            x_axis_title='Date', 
                            y_axis_title='revenue',
                            trend_1='Revenue', 
                            trend_2='Revenue',
                            key='tab1_1')

    # st.text('Revenue trend & comparison with the previous period - Cumulative')
    # st.markdown(f'**Revenue trend & comparison with the previous period - Cumulative**', help = 'definition')  
    header_chart('Revenue trend & comparison with the previous period - Cumulative') 
    get_trendline_charts(df=tab_1,
                            df_delta=tab_1_delta,
                            date_col='OrderDate', 
                            x_axis_title='Date', 
                            y_axis_title='revenue',
                            trend_1='Cumulative_Revenue', 
                            trend_2='Cumulative_Revenue',
                            key='tab1_2')


    # st.text('Total Orders trend and Comparison with the previous period')  
    # st.markdown(f'**Total Orders trend and Comparison with the previous period**', help = 'definition')  
    header_chart('Total Orders trend and Comparison with the previous period')
    # trend_comparison_line_chart()
    get_trendline_charts(df=tab_1,
                            df_delta=tab_1_delta,
                            date_col='OrderDate', 
                            x_axis_title='Date', 
                            y_axis_title='Orders',
                            trend_1='Total_Orders', 
                            trend_2='Total_Orders',
                            key='tab1_3')

    # st.text('Average Order Value trend and Comparison with the previous period')   
    # st.markdown(f'**Average Order Value trend and Comparison with the previous period**', help = 'definition') 
    header_chart('Average Order Value trend and Comparison with the previous period')
    # trend_comparison_line_chart()
    get_trendline_charts(df=tab_1,
                            df_delta=tab_1_delta,
                            date_col='OrderDate', 
                            x_axis_title='Date', 
                            y_axis_title='AOV',
                            trend_1='AOV', 
                            trend_2='AOV',
                            key='tab1_4')


    # st.text('New Customers trend and Comparison with the previous period')
    # st.markdown(f'**New Customers trend and Comparison with the previous period**', help = 'definition') 
    header_chart('New Customers trend and Comparison with the previous period')
    get_trendline_charts(df=tab_1,
                            df_delta=tab_1_delta,
                            date_col='OrderDate', 
                            x_axis_title='Date', 
                            y_axis_title='New Customers',
                            trend_1='Total_New_Customers', 
                            trend_2='Total_New_Customers',
                            key='tab1_5')