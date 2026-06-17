# Gas Trading

Variable	Type	Describe
natgas_df	DataFrame	Dates and Prices data
date_int	integer	Data in numerical form (datetime64)
price_vals	float	array of prices


## Purpose:
- A pricer model that estimate how much a trade worth if we buy energy during summer when the price are cheap and sell it in the winter when the price have increased.

## Data:
- Monthly natural gas prices. Each data point is:
    + the market purchase price of natural gas.
    + for delivery at the end of that month.
    + from 31/10/2020 to 30/09/2024

## Analyze Price Data: 
### Objective:
 1. Estmiate the purchase price for any data in the past (Interpolate).
 2. Extrapolate prices for one more year beyong the last available month-end point
 3. Provide a function to input a date => output an estimated price

### Steps: 
1. Interpolation:
    - Use observed month-end prices as anchor data points.
    - Assume prices evolve smoothly between consecutive month-end observations.
    - Apply linear interpolation to estimate prices for any date within the historical range.
    - Build a function that accepts a historical date and returns the interpolated price.
3. Extrapolation:
    - Analyse historical data to identify trend and seasonal patterns.
    - Model the underlying price trend using time-based regression.
    - Capture annual seasonality using trigonometric (sine and cosine) components.
    - Fit the model to historical monthly prices.
    - Use the fitted model to forecast prices up to one year beyond the last observed date.
    - Integrate interpolation and extrapolation into a single pricing function.

### Output:
<img width="392" height="278" alt="image" src="https://github.com/user-attachments/assets/ae59a239-492b-4e97-a17a-7cfad08cf5bc" />
<img width="382" height="278" alt="image" src="https://github.com/user-attachments/assets/6d4e6ccd-2fd7-4b50-b859-87decaaf3311" />
<img width="615" height="333" alt="image" src="https://github.com/user-attachments/assets/86ceeebd-7302-4d25-a12e-2a5d4020e633" />
<img width="727" height="387" alt="image" src="https://github.com/user-attachments/assets/8f41a141-936a-4b0c-91a3-f6c722b0cd17" />

## Contract Valuation:
### Context: 
- Any trade agreement is as valuable as:
    The price we can sell - The price we are able to buy - cost
- Profit <= Sell > Price + Cost
- Example: Purchase in summer at MMBtu $2/MMBtu and store for 4 months, and ensure to sell at $3/MMBtu, with $0.1 Storage cost per month, $0.01 injection/withdrawal cost per 1MMBtu and $0.05 transportation cost to and from facility.

=> Value of contract = (3-2) - 0.1* 4 - 0.01 - 0.05* 2 = 0.490 ($)
- Storage Trade Process:
    + Buy (Injection Date) => Outflow = Injected * Buy Price
    + Store.
    + Sell (Withdrawal Date) => Inflow = Withdraw * Sell Price    
  
### Needed Inputs:
- Injection dates
- Withdrawal dates
- Volumes injected/withdrawn
- Injection and withdrawal rate limits
- Maximum storage capacity
- Storage cost (per month)
- Injection/withdrawal fees
- Transportation cost

### Steps:
1. Identify all injection and withdrawal dates and volumes.
2. Arrange all contract events in chronological order.
3. Track inventory levels dynamically over time.
4. Apply storage costs for the duration gas remains stored.
5. Calculate injection cash outflows (purchase price + fees + transport).
6. Calculate withdrawal cash inflows (sale price − fees − transport).
7. Enforce operational constraints (rate limits and capacity).
8. Aggregate all cash flows to determine total contract value.

### Output (Example):
<img width="551" height="269" alt="image" src="https://github.com/user-attachments/assets/04fda629-9a1c-43ac-b3f1-3ca544b2d9e1" />
<img width="1016" height="144" alt="image" src="https://github.com/user-attachments/assets/27d0f3e5-79c9-43f3-b7ff-fa83821ffc28" />

