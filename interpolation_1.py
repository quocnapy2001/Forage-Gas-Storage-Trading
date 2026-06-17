# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 08:06:16 2026

@author: Owner
"""

# Description: Since the data provided is only monthly
# so it order to get daily price, linear interpolation
# is used since it is defensible, simple and consistent

# Interpolation for this case mean that it assumed the 
# best neutral guess for any date between 2 observed
# month-end prices is a straight line.

from data_0 import natgas_df, pd, plt, np


date_int = natgas_df["Dates"].values.astype("datetime64[D]").astype(int)
price_vals = natgas_df["Prices"].values

def interpolate_price(query_date):
    q = pd.to_datetime(query_date)
    q_int = q.to_datetime64().astype("datetime64[D]").astype(int)
    return float(np.interp(q_int, date_int, price_vals))

# Test
print("/")
print("Interpolation check (15/12/2022):",interpolate_price("2022-11-15"))

