# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 07:27:01 2026

@author: Owner
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------
# Data Import
# ---------------------------------------------------------
natgas_df = pd.read_csv("Nat_Gas.csv")
natgas_df["Dates"] = pd.to_datetime(natgas_df["Dates"])

prices = natgas_df["Prices"].values
dates = natgas_df["Dates"]


print(natgas_df)


# ---------------------------------------------------------
# Data Visualize
# ---------------------------------------------------------
plt.figure()
plt.plot(natgas_df["Dates"], natgas_df["Prices"], marker="o")
plt.title("Monthly Natural Gas Prices (Month-End Delivery)")
plt.xlabel("Date")
plt.ylabel("Price")
plt.grid(True)
plt.show()

# Average price by calendar month
natgas_df["Month"] = natgas_df["Dates"].dt.month
month_avg = natgas_df.groupby("Month")["Prices"].mean()

plt.figure()
plt.bar(month_avg.index, month_avg.values)
plt.title("Average Price by Month of Year (Seasonality Check)")
plt.xlabel("Month (1=Jan, ..., 12=Dec)")
plt.ylabel("Average Price")
plt.grid(axis="y")
plt.show()
