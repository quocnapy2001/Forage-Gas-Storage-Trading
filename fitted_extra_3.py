# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 01:05:09 2026

@author: Owner
"""


from data_0 import pd, plt, dates, prices
from extrapolation_2 import forecast_limit, model, make_features, last_date, estimate_gas_price

# ---------------------------------------------------------
# Create Full Daily Timeline (Observed + Forecast)
# ---------------------------------------------------------
full_dates = pd.date_range(
    start=dates.min(),
    end=forecast_limit,
    freq="D"
)

full_model_values = model.predict(make_features(full_dates))


# ---------------------------------------------------------
# 7. Plot Observed + Fitted + Forecast
# ---------------------------------------------------------
plt.figure(figsize=(12, 6))

# Observed monthly prices
plt.scatter(
    dates,
    prices,
    label="Observed Monthly Prices",
    zorder=3
)

# Model fitted + forecast curve
plt.plot(
    full_dates,
    full_model_values,
    color="orange",
    label="Model Fitted + Forecast"
)

# Boundary line
plt.axvline(
    last_date,
    linestyle="--",
    color="grey",
    label="End of Observed Data"
)

plt.title("Natural Gas Prices: Observed vs Model Fit and Forecast")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()


# ---------------------------------------------------------
# Test Queries
# ---------------------------------------------------------
print("\n--- Price Estimates (Fitted) ---")
print("Past date (31/12/2022):", estimate_gas_price("2022-12-31"))
print("Last observed (30/09/2024):", estimate_gas_price("2024-09-30"))
print("Future date (30/04/2025):", estimate_gas_price("2025-04-30"))