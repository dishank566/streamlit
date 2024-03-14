# Worst cohorts
from src.charts.tile import kpi_tile, header, header_chart, header_left, header_pie
from src.charts.charts import horizontal_bar_chart_with_value, trend_comparison_line_chart, trend_comparison_line_chart_aov, grouped_bar_chart_with_line_chart_2, bar_chart_with_line_chart, pie_chart, pie_chart_2, grouped_bar_chart, grouped_bar_chart_groupby, get_trendline_charts

# pending bq table

def tab__5(table_dict,option):
    
    header('Worst Cohort View')

    # st.text('Worst Channel Cohorts')
    header_chart('Worst Channel Cohorts')
    bar_chart_with_line_chart(table_dict['mts_customer_profile_by_channel'], 'MarketingChannel', 'Channel')
    
    # st.text('Worst City Cohorts')
    header_chart('Worst City Cohorts')
    bar_chart_with_line_chart(table_dict['mts_city_level_cv90'], 'CustomerCity', 'City', threshold=20)

    