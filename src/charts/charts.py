import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import altair as alt
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
# import matplotlib.pyplot as plt

# Bar and line chart in one
def default_chart(chart_title,chart_key,chart_df,chart_height=630, radio_horizontal=True, color_theme='streamlit'):
    with st.container(height=chart_height):
        st.markdown(f'**{chart_title}**')
        col_1, col_2 = st.columns([4,1])
        with col_2:
            chart_type = st.radio(
                "",
                ["Line Chart", "Bar Chart"], horizontal=radio_horizontal, key=chart_key)

        if chart_type == 'Line Chart':
            fig = px.line(data_frame=chart_df) # chart_df=df.groupby('Purchase Date')['Net Sales'].sum()
        else:
            fig = px.bar(data_frame=chart_df)

        fig.update(layout_showlegend=False)
        # fig.update_traces(line=dict(color="Yellow", width=0.4))

        st.plotly_chart(fig, theme=color_theme, use_container_width=True)


def horizontal_bar_chart_with_value(data, col_1):
    if 'Total_Price' not in data.columns:
        data['Total_Price'] = data['ItemQuantity'] * data['Item_UnitPrice']
    data_1=data.groupby(col_1)['Total_Price'].sum().to_frame()
    data = data_1.sort_values(by='Total_Price', ascending=False).head(10)
    data = data.reset_index()

    # Altair chart with horizontal bars and totals
    chart = alt.Chart(data).mark_bar().encode(
        x='Total_Price:Q',
        # y='ItemName:N',
        y=alt.Y(f'{col_1}:N', sort=alt.EncodingSortField(field='Total_Price', op='sum', order='descending')),
        tooltip=[f'{col_1}:N', 'Total_Price:Q']
    )

    text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Offset for text placement to the right of bars
    ).encode(
        text='Total_Price:Q'
    )

    chart_with_text = (chart + text).properties(
        height=alt.Step(50)  # Adjust the height of the bars
    )

    # Streamlit display
    st.altair_chart(chart_with_text, use_container_width=True)

def trend_comparison_line_chart(df,df_delta,date_col, col_1 ,x_axis_title, y_axis_title,trend_1, trend_2, key, cumulative_sum=False, unique_count=False, new_customer=False):
    granularity_dict = {'Daily': 'D','Weekly': 'W', 'Monthly': 'ME', 'Yearly': 'YE'}
    _,_,_,col = st.columns(4)
    with col:
        gran = st.selectbox('Granularity', ('Daily', 'Weekly', 'Monthly', 'Yearly'), key=key)

    if df.index.name != date_col and df_delta.index.name != date_col:
        df.set_index(date_col, inplace=True)
        df_delta.set_index(date_col, inplace=True)
    if new_customer:
        df= df[df.index == df['FirstOrderDate']][col_1]
        df_delta= df_delta[df_delta.index == df_delta['FirstOrderDate']][col_1]
        df = df.to_frame()
        df_delta = df_delta.to_frame()
    if unique_count:
        df = df.groupby(date_col)[col_1].nunique().to_frame()
        df_delta = df_delta.groupby(date_col)[col_1].nunique().to_frame()
    df = df[[col_1]].resample(granularity_dict[gran]).sum()
    df_delta = df_delta[[col_1]].resample(granularity_dict[gran]).sum()
    if cumulative_sum:
        df['Cumulative_Value'] = df[col_1].cumsum()
        df_delta['Cumulative_Value'] = df_delta[col_1].cumsum()
        col_1 = 'Cumulative_Value'
    time_frame = df.index.to_list() # change timeframe
    trend1_values = df[col_1].to_list()
    trend2_values = df_delta[col_1].to_list()

    time_frame_delta = df_delta.index.to_list()

    # Create traces for each trend
    trace1 = go.Scatter(x=time_frame, y=trend1_values, mode='lines+markers', name=f'{trend_1}_{gran}', xaxis='x')
    trace2 = go.Scatter(x=time_frame_delta, y=trend2_values, mode='lines+markers', name=f'{trend_2}_{gran}_previous',xaxis='x2' )

    # Create layout
    layout = go.Layout(
        # title='Trend Comparison Chart',
        xaxis=dict(title=x_axis_title),
        xaxis2=dict(title='Secondary X-Axis Title', overlaying='x', side='top', visible=False),  # Add a secondary x-axis
        yaxis=dict(title=y_axis_title),
    )


    # Create figure
    # fig = go.Figure(data=[trace1, trace2], layout=layout)
    fig = go.Figure(layout=layout)
    fig.add_trace(trace1)
    fig.add_trace(trace2)

    # Show the figure
    # fig.show()
    st.plotly_chart(fig, use_container_width=True)

def trend_comparison_line_chart_aov(df,df_delta,date_col, col_1 ,col_2,x_axis_title, y_axis_title,trend_1, trend_2, key, cumulative_sum=False, unique_count=False):
    df2=df
    df2_delta = df_delta
    granularity_dict = {'Daily': 'D','Weekly': 'W', 'Monthly': 'ME', 'Yearly': 'YE'}
    _,_,_,col = st.columns(4)
    with col:
        gran = st.selectbox('Granularity', ('Monthly', 'Yearly'), key=key)
    if df.index.name != date_col and df_delta.index.name != date_col:
        df.set_index(date_col, inplace=True)
        df_delta.set_index(date_col, inplace=True)

    df = df[[col_1]].resample(granularity_dict[gran]).sum()
    df_delta = df_delta[[col_1]].resample(granularity_dict[gran]).sum()

    time_frame = df.index.to_list() # change timeframe
    trend1_values = df[col_1].to_list()
    trend2_values = df_delta[col_1].to_list()

    if df2.index.name != date_col and df2_delta.index.name != date_col:
        df2.set_index(date_col, inplace=True)
        df2_delta.set_index(date_col, inplace=True)
    if unique_count:
        df2 = df2.groupby(date_col)[col_2].nunique().to_frame()
        df2_delta = df2_delta.groupby(date_col)[col_2].nunique().to_frame()
    df2 = df2[[col_2]].resample(granularity_dict[gran]).sum()
    df2_delta = df2_delta[[col_2]].resample(granularity_dict[gran]).sum()

    # time_frame = df2.index.to_list() # change timeframe
    trend1_values2 = df2[col_2].to_list()
    trend2_values2 = df2_delta[col_2].to_list()
    
    y1 = [a / b for a, b in zip(trend1_values, trend1_values2)]
    y2 = [a / b for a, b in zip(trend2_values, trend2_values2)]
    # Create traces for each trend
    trace1 = go.Scatter(x=time_frame, y=y1, mode='lines+markers', name=f'{trend_1}_{gran}')
    trace2 = go.Scatter(x=time_frame, y=y2, mode='lines+markers', name=f'{trend_2}_{gran}')

    # Create layout
    layout = go.Layout(
        # title='Trend Comparison Chart',
        xaxis=dict(title=x_axis_title),
        yaxis=dict(title=y_axis_title),
    )

    # Create figure
    fig = go.Figure(data=[trace1, trace2], layout=layout)

    # Show the figure
    # fig.show()
    st.plotly_chart(fig, use_container_width=True)


def grouped_bar_chart_with_line_chart_2(data, group_by):
    # Ecom_Ordertable = data
    data.reset_index(inplace=True)
    data['Order_interval'] = (pd.to_datetime(data['OrderDate']) - pd.to_datetime(data['FirstOrderDate'])).dt.days

    data['Month'] = pd.to_datetime(data['OrderDate']).dt.strftime('%Y-%m')

    data['CV_1'] = np.where(data['Order_interval'] < 2, data['Total_Price'], 0)
    data['CV_30'] = np.where(data['Order_interval'] < 31, data['Total_Price'], 0)
    data['CV_60'] = np.where(data['Order_interval'] < 61, data['Total_Price'], 0)
    data['CV_90'] = np.where(data['Order_interval'] < 91, data['Total_Price'], 0)
    data['CV_180'] = np.where(data['Order_interval'] < 181, data['Total_Price'], 0)
    plot = px.bar(data.groupby([group_by])[['CV_1','CV_30', 'CV_60', 'CV_90', 'CV_180']].mean(),
       barmode='group'
      )

    st.plotly_chart(plot, use_container_width=True)

def bar_chart_with_line_chart(data, var,x_title, threshold=None):
    # data['total'] = data['CV_90'] * data['customer_count']
    # data = data.groupby(var)[['total','customer_count']].sum().reset_index()
    # data['CV90'] = data['total']/data['customer_count']
    if threshold:
        data = data[data['TotalCustomers']>threshold]
    if data.shape[0] >= 10:
        data_sorted = data.sort_values(by='AvgCV_90', ascending=True).reset_index()
        data_sorted = data_sorted.head(10)
    else:
        data_sorted = data.sort_values(by='AvgCV_90', ascending=True).reset_index()
    x = data_sorted[var]
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces for each y-axis
    fig.add_trace(go.Bar(x=x, y=data_sorted['AvgCV_90'], name='CV90'), secondary_y=False)
    fig.add_trace(go.Line(x=x, y=data_sorted['TotalCustomers'], name='Total Customers'), secondary_y=True)

    # Update layout with axis labels
    fig.update_layout(
        xaxis=dict(title=x_title),
        yaxis=dict(title='Value', side='left'),
        yaxis2=dict(title='Number of Customers', side='right')
    )

    # plot = go.Figure(data=[go.Bar(
    #     name = 'CV90',
    #     x = x,
    #     y = data['CV90'].to_list(),
    # ),
    #     go.Line(
    #     name= 'CustomerID',
    #     x=x,
    #     y=data['customer_count'].to_list(),
    # )
    # ])
                    
    st.plotly_chart(fig, use_container_width=True)

def pie_chart(df, var, values, desired_order):
    cat_pie = px.pie(df,
                    names=var,
                    hole=0.5,
                    color=var,
                    values=values,
                    category_orders={var: desired_order}
                )
    # cat_pie.update_layout(showlegend=True)
    st.plotly_chart(cat_pie, theme='streamlit', use_container_width=True)

def pie_chart_2(df, var, desired_order):
    cat_pie = px.pie(data_frame=df.groupby(var)['CustomerID'].nunique().to_frame().reset_index(),
                    names=var,
                    hole=0.5,
                    color=var,
                    values='CustomerID',
                    category_orders={var: desired_order}
                )
    # cat_pie.update_layout(showlegend=True)
    st.plotly_chart(cat_pie, theme='streamlit', use_container_width=True)

def grouped_bar_chart(data, index, option, value_column_name ,st_date, column_name=None, agg_func='mean', desired_order=None):    
    if option=='All Data':
        pass
    else:
        try:
            data['OrderDate'] = pd.to_datetime(data['OrderDate'])
            data = data[data['OrderDate']>st_date]
        except:
            data['FirstOrderDate'] = pd.to_datetime(data['FirstOrderDate'])
            data = data[data['FirstOrderDate']>st_date]
    plot = px.bar(data.pivot_table(index=index, 
                                columns=column_name,
                                values=value_column_name,
                                aggfunc= agg_func
                                )[desired_order],
    
    barmode='group')
    st.plotly_chart(plot, use_container_width=True)

def grouped_bar_chart_groupby(data, group_by, column_name, index, option, desired_order=None):
    plot = px.bar(data.groupby(group_by)[column_name].value_counts().reset_index(),
    x=index,
    y='count',
    color=column_name,
    barmode='group',
    category_orders={column_name: desired_order}
    )
    st.plotly_chart(plot, use_container_width=True)


def get_trendline_charts(df,
                        df_delta,
                        date_col, 
                        x_axis_title, 
                        y_axis_title,
                        trend_1,
                        trend_2,
                        key):
    
    granularity_dict = {'Daily': 'D',
                        'Weekly': 'W', 
                        'Monthly': 'ME',
                        'Yearly': 'YE'}
    
    _,_,_,col = st.columns(4)
    
    with col:
        gran = st.selectbox('Granularity', ('Daily', 'Weekly', 'Monthly', 'Yearly'), key=key)
        
    if df.index.name != date_col and df_delta.index.name != date_col:
        
        df.set_index(date_col, inplace=True)
        df_delta.set_index(date_col, inplace=True)
        
    if (not df.index.dtype.name.startswith('date')) and (not df_delta.index.dtype.name.startswith('date')):
        
        df = df.reset_index().assign(**{date_col : lambda x: pd.to_datetime(x[date_col])}).set_index(date_col)
        df_delta = df_delta.reset_index().assign(**{date_col : lambda x: pd.to_datetime(x[date_col])}).set_index(date_col)
        
        
    df = df.resample(granularity_dict[gran]).sum()
    df_delta = df_delta.resample(granularity_dict[gran]).sum()
        
    trend1_values = df[trend_1].to_list()
    trend2_values = df_delta[trend_2].to_list()
    
    time_frame = df.index.to_list()
    time_frame_delta = df_delta.index.to_list()

    # Create traces for each trend
    trace1 = go.Scatter(x=time_frame, y=trend1_values, mode='lines+markers', name=f'{trend_1}_{gran}', xaxis='x')
    trace2 = go.Scatter(x=time_frame_delta, y=trend2_values, mode='lines+markers', name=f'{trend_2}_{gran}_previous',xaxis='x2' )

    # Create layout
    layout = go.Layout(
        # title='Trend Comparison Chart',
        xaxis=dict(title=x_axis_title),
        xaxis2=dict(title='Secondary X-Axis Title', overlaying='x', side='top', visible=False),  # Add a secondary x-axis
        yaxis=dict(title=y_axis_title),
    )
    fig = go.Figure(layout=layout)
    fig.add_trace(trace1)
    fig.add_trace(trace2)
    
    st.plotly_chart(fig, use_container_width=True)