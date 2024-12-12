import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn


def summary_statistics(df):
  """
  Shows the men, median, standard deviation, and the like of the dataset

  Accepts dataframe as an argument
  """
  df.describe()
