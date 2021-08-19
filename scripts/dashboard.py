import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import streamlit as st
import os
from sklearn.linear_model import LinearRegression

sns.set_theme()


# utility functions

def compute_ts_correlation( start_year, end_year, country_1, country_2, metric ):
  df_base = df.loc[(df['year'] >= start_year) & (df['year'] < end_year)]

  df_1 = df_base[ df_base['country'] == country_1 ]
  df_2 = df_base[ df_base['country'] == country_2 ]

  r, p = stats.pearsonr( df_1[metric], df_2[metric] )

  return r, p


def compute_ts_block_correlation( country_1, country_2, metric, time_periods ):
  outputs = []

  for period in time_periods:
    r, p = compute_ts_correlation( period[0], period[1], country_1, country_2, metric )

    outputs.append( [r, p] )
  
  return outputs

def get_average_correlation( metric, countries, time_periods ):
  used_countries = []
  correlations = [ [], [] ]
  out = []

  for country_1 in countries:
    used_countries.append( country_1 )

    for country_2 in countries:

      if country_2 in used_countries:
        continue

      if country_1 == country_2:
        continue

      outputs = compute_ts_block_correlation( country_1, country_2, metric )

      for i in range( 0, len(time_periods) ):
        correlations[i].append( abs(outputs[i][0]) )

  for period in correlations:
    total = 0

    for correlation in period:

      total += correlation

    out.append( total / len(period) )

  return out, correlations


def pivot_plot( df, values, index, columns, countries ):
  pivot = df.pivot_table( values=values, index=index, columns=columns )

  fig, ax = plt.subplots()

  if countries == 'all':
    countries = df['country'].unique()

  for country in countries:
    filt_df = df[ df['country'] == country ]

    ax.plot( filt_df[index], filt_df[values], label=country )

  ax.set_xlabel(index)
  ax.set_ylabel(values)

  fig.suptitle( values + ' vs ' + index )

  ax.legend()

  st.pyplot(fig)


# import data
df = pd.read_csv("./data/econ_data.csv")

countries = df['country'].unique()
metrics = df.columns[3:]

# sidebar
selected_countries = st.sidebar.multiselect(
  'Select Countries',
  countries,
  countries
)

selected_metric = st.sidebar.selectbox(
  'Select Metric',
  metrics
)


# title
st.title('World Economies')

st.write(
'''This app dashboard was build to visualize how globalization has 
progressed since the 1990s'''
)

pivot_plot( df, selected_metric, 'year', 'country', selected_countries )