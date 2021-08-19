import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import streamlit as st
import os
from sklearn.linear_model import LinearRegression

sns.set_theme()


# STAT FUNCTIONS

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

# PLOTTING FUNCTIONS

def line_plot( df, values, index, countries, years ):
  fig, ax = plt.subplots()
  
  for country in countries:
    filt_df = df[ df['country'] == country ]
    filt_df = filt_df[ ( filt_df['year'] >= years[0] ) & ( filt_df['year'] <= years[1] ) ]
  
    ax.plot( filt_df[index], filt_df[values], label=country )

  ax.set_xlabel(index)
  ax.set_ylabel(values)

  fig.suptitle( values + ' vs ' + index )
  fig.set_size_inches( 10, 6 )

  ax.legend()

  st.pyplot(fig)


def swarmplot( df, values, index, countries, years ):
  fig, ax = plt.subplots()

  fig.suptitle( values + ' vs ' + index )
  fig.set_size_inches( 10, 6 )

  filt_df = df[ ( df['year'] >= years[0] ) & ( df['year'] <= years[1] ) ]

  sns.swarmplot( ax=ax, x='country', y=values, data=filt_df )

  ax.set_xlabel(index)
  ax.set_ylabel(values)

  st.pyplot(fig)


# IMPORT DATA
df = pd.read_csv("./data/econ_data.csv")

countries = df['country'].unique()
metrics = df.columns[4:]

# STREAMLET

# side bar
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
  '''This app dashboard was build to visualize how globalization has progressed
  since the 1990s.'''
)

# distribution
st.write("# Distribution")

st.write(
  '''This section display distributions in the selected metric for each country.
  Each year (or change between them) is represented by a dot.'''
)

ds_years = st.slider(
  'Select Years for Distribution',
  1992,
  2020,
  (1992, 2020)
)

swarmplot( df, selected_metric, 'year', selected_countries, ds_years )

# time series
st.write("# Time Series")

st.write(
  '''This section displays lineplots of the selected metric over time for each
  country.'''
)

ts_years = st.slider(
  'Select Years for Timeseries',
  1992,
  2020,
  (1992, 2020)
)

line_plot( df, selected_metric, 'year', selected_countries, ts_years )

# timeseries correlation
st.write("# Time Series Correlation")

st.write(
  '''This section shows the average correlation between the selected countries
  for five year periods.'''
)

