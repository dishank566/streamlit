import streamlit as st

def kpi_tile(kpi,tile_text,tile_label,tile_value,delta_value,option,delta_value_suffix='%',delta_color_inversion='normal',
             tile_height=190,tile_value_suffix='', tile_value_prefix='', integer = False, help='definition'):
     tile = kpi.container(height=tile_height)
     tile.markdown(f'**{tile_text}**', help = help)
     tile_value_updated = [f'{tile_value:,.0f}' if integer else f'{tile_value:,.2f}']
     if option != 'All Data':
          tile.metric(label=tile_label, value=f"{tile_value_prefix}{tile_value_updated[0]}{tile_value_suffix}",
                delta=f'{delta_value:,.1f}{delta_value_suffix}',delta_color=delta_color_inversion)
     else:
          tile.metric(label=tile_label, value=f"{tile_value_prefix}{tile_value_updated[0]}{tile_value_suffix}")

def header(url, size=24):
     my_container = st.container(height=size*3)
     my_container.markdown(f'<p style="color:#000000;font-size:{size}px;text-align:center; font-weight: bold;">{url}</p>', unsafe_allow_html=True)
    #  st.markdown(f'<p style="background-color:#0066cc;color:#FFFFFF;font-size:24px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def header_chart(url, size=24):
     my_container = st.container(height=size*3)
     my_container.markdown(f'<p style="color:#000000;font-size:{size}px;border-radius:2%;text-align:center; font-weight: bold;">{url}</p>', unsafe_allow_html=True)

def header_left(url, size=24):
     st.markdown(f'<p style="color:#000000;font-size:{size}px;border-radius:2%;text-align:left; font-weight: bold;">{url}</p>', unsafe_allow_html=True)

def header_pie(url, size=14):
     my_container = st.container(height=55)
     my_container.markdown(f'<p style="color:#000000;font-size:{size}px;text-align:center; font-weight: bold;">{url}</p>', unsafe_allow_html=True)