import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import streamlit
from sklearn.linear_model import LinearRegression

sns.set_theme()

# import data
df = pd.read_csv('../data/econ_data')

st.title('World Economies')

st.write('''This app dashboard was build to visualize how globalization has 
progressed since the 1990s''')