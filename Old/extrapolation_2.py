# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 12:58:03 2026

@author: Owner
"""

# Due to the data chacteristics => should include seasonality

from data_0 import natgas_df, pd, plt, np
from interpolation_1 import interpolate_price
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

### Prepare for Extrapolation
start_date = natgas_df["Dates"].min()

def make_features(dates):
    dates = pd.Series(pd.to_datetime(dates))
    
    # Trend
    t = (dates - start_date).dt.days.values.reshape(-1, 1)
    t2 = t ** 2
    
    # Seasonality
    m = dates.dt.month.values.reshape(-1, 1)
    angle = 2 * np.pi * m / 12
    
    sin1 = np.sin(angle)
    cos1 = np.cos(angle)
    
    return np.hstack([t, t2, sin1, cos1])

### Regression Model for Extrapolation
X = make_features(natgas_df["Dates"])
y = natgas_df["Prices"].values

model = Pipeline([
    ("scaler", StandardScaler()),
    ("ridge", Ridge(alpha=1.0))
])

model.fit(X, y)


### Unified Pricing Function
last_date = natgas_df["Dates"].max()
forecast_limit = last_date + pd.Timedelta(days=365)

def estimate_gas_price(date_input):
    q = pd.to_datetime(date_input)
    
    if q <= last_date:
        return interpolate_price(q)
    
    if q <= forecast_limit:
        Xq = make_features([q])
        return float(model.predict(Xq)[0])
    
    raise ValueError("Date beyond supported forecast horizon")
    
    
### Plot Extrapolation 1 Year
future_dates = pd.date_range(
    start=last_date,
    end=forecast_limit,
    freq="D"
)

future_predicted = model.predict(make_features(future_dates))

plt.figure(figsize=(10, 5))

# Observed (actual) – connected line, blue
plt.plot(
    natgas_df["Dates"],
    natgas_df["Prices"],
    marker="o",
    label="Observed market prices"
)

# Predicted (future only) – orange
plt.plot(
    future_dates,
    future_predicted,
    color="orange",
    label="Predicted prices (extrapolation)"
)

# Boundary between actual and predicted
plt.axvline(
    last_date,
    linestyle="--",
    color="grey",
    label="End of observed data"
)

plt.title("Natural Gas Prices: Observed vs Predicted")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()

### Test
print("\n--- Price Estimates ---")
print("Past date (31/12/2022):", estimate_gas_price("2022-12-31"))
print("Last observed (30/09/2024):", estimate_gas_price("2024-09-30"))
print("Future date (30/04/2025):", estimate_gas_price("2025-04-30"))