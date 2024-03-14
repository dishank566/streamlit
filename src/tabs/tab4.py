# Best Customer Profile
import streamlit as st
import pandas as pd
from src.charts.tile import kpi_tile, header, header_chart, header_left, header_pie
from src.charts.charts import horizontal_bar_chart_with_value, trend_comparison_line_chart, trend_comparison_line_chart_aov, grouped_bar_chart_with_line_chart_2, bar_chart_with_line_chart, pie_chart, pie_chart_2, grouped_bar_chart, grouped_bar_chart_groupby, get_trendline_charts

def tab__4(table_dict):
    # customer_profile_by_channel_comparison = pd.read_csv('src/data/customer_profile_by_channel_comparison.csv')
    # st.text('Best Vs Average Customer Profile - Comparison View')
    header('Best Vs Average Customer Profile - Comparison View')
    header_chart('Customer Profile by Channel Comparison View')
    # df_demo = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))
    # customer_profile_by_channel_comparison= customer_profile_by_channel_comparison.groupby('marketing_channel').agg({'SecondOrdValue':'mean', 'D2_D1':'mean', 'First_Ord_Value':'mean', 'CV_90':'mean', 'CustomerID':'count'})
    # customer_profile_by_channel_comparison['D2_D1'] = customer_profile_by_channel_comparison['D2_D1'].abs().apply(lambda x: int(x))
    # customer_profile_by_channel_comparison = customer_profile_by_channel_comparison.astype(int)
    data = table_dict['mts_customer_profile_by_channel']
    data = data.fillna(0)
    numeric_columns = data.select_dtypes(include='number').columns
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce').astype('int')
    st.dataframe(data, use_container_width=True, hide_index=True)
    # with st.container(height=600):
        
    header_chart('Product Level Profile by Channel')
    # df_demo = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))
    # st.dataframe(df_demo)  
    #dataframe here
    # data = pd.read_csv('src/data/df.csv')
    # data_2 = pd.read_csv('src/data/df_part2.csv')
    # data_3 = pd.read_csv('src/data/df_part3.csv')
    # data = pd.concat([data_1, data_2, data_3], ignore_index=True)
    _,_,_,col_4 = st.columns(4)
    with col_4:
        channel_filter = st.selectbox('Channel:',table_dict['mts_customer_profile_by_product']['marketing_channel'].unique(),key='tab4_22')
        data = table_dict['mts_customer_profile_by_product']
        data = data[data['marketing_channel']==channel_filter]
        data = data[data['TotalOrders']>10][['ItemName', 'TotalOrders', 'AOV']].sort_values('AOV', ascending=False)
    
    # data['Total_price'] = data['ItemQuantity'] * data['Item_UnitPrice']
    # data = data.groupby('ItemName').agg({'Total_price':'mean', 'OrderID':'count'})
    # data['avg order value'] = data['Total_price']/data['OrderID']
    # data = data.drop(columns=['Total_price']).rename({'OrderID': 'customer count'}).sort_values(by='avg order value', ascending=False)
    # data = data[data['OrderID']>0]
    # data['avg order value'] = data['avg order value'].apply(lambda x : int(x))
        
    # st.dataframe(data, use_container_width=True)
    data['AOV'] = data['AOV'].astype(int)
    st.dataframe(data, use_container_width=True,hide_index=True)