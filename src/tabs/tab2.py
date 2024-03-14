# Customer value cohort
import streamlit as st
import plotly.express as px
import pandas as pd
from src.charts.tile import kpi_tile, header, header_chart, header_left, header_pie
from src.charts.charts import horizontal_bar_chart_with_value, trend_comparison_line_chart, trend_comparison_line_chart_aov, grouped_bar_chart_with_line_chart_2, bar_chart_with_line_chart, pie_chart, pie_chart_2, grouped_bar_chart, grouped_bar_chart_groupby, get_trendline_charts

def tab__2(table_dict, option, st_date):

    header('How valuable are our Customers over time?')
        
    header_chart('How Many Customers repeat?')

    data = table_dict['mts_cv_daily']
    data['FirstOrderDate'] = pd.to_datetime(data['FirstOrderDate'])
    data = data.set_index('FirstOrderDate')
    data = data.resample('M').sum().reset_index()
    data = data.assign(CV_1=data['CV_1_DAILY'] / data['CV_1_CC_DAILY'],
                    CV_30=data['CV_30_DAILY'] / data['CV_30_CC_DAILY'],
                    CV_60=data['CV_60_DAILY'] / data['CV_60_CC_DAILY'],
                    CV_90=data['CV_90_DAILY'] / data['CV_90_CC_DAILY'],
                    CV_180=data['CV_180_DAILY'] / data['CV_180_CC_DAILY'])
    data = data[['FirstOrderDate', 'CV_1', 'CV_30', 'CV_60', 'CV_90','CV_180']]
    data = data.melt(id_vars='FirstOrderDate',
                    value_vars=['CV_1', 'CV_30', 'CV_60', 'CV_90','CV_180'],
                    var_name='CV_Span',
                    value_name='Average Customer Value',
                    )
    if option=='All Data':
        pass
    else:
        data = data[data['FirstOrderDate']>st_date]

    data['FirstOrderDate'] = data['FirstOrderDate'].dt.strftime("%b'%y")
    fig = px.bar(data,
                x='FirstOrderDate',
                y='Average Customer Value',
                color='CV_Span',
                barmode='group'
                )
    st.plotly_chart(fig, use_container_width=True)



    header_chart('Average Customer Value by Marketing Channel over 1/30/60/90/180 days time period')

    fig = px.bar((table_dict['mts_avg_cv_by_marketing_channel'].set_index('marketing_channel')
                    [['CV_1','CV_30','CV_60','CV_90', 'CV_180']]),
                    barmode='group'
                    )
    st.plotly_chart(fig, use_container_width=True)

