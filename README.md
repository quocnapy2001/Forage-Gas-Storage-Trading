# Gas Trading

|Variable|Type|Describe|
|-|-|-|
|natgas\_df|DataFrame|Dates and Prices data|
|date\_int|integer|Data in numerical form (datetime64)|
|price\_vals|float|array of prices|
|start\_date||earliest date in the date|



|Function|Describe|
|-|-|
|interpolate\_price(query\_date)|Estimate the price of the chosen date or query\_date|
|make\_features(dates)|Combine a matrix of trend, trend curvature and seasonality. |
|||



## Purpose:

* A pricing model that estimates how much a trade is worth if we buy energy during summer when prices are low and sell it in the winter when prices have increased.

## Data:

* Monthly natural gas prices. Each data point is:

  * The market purchase price of natural gas.
  * for delivery at the end of that month.
  * from 31/10/2020 to 30/09/2024

## Analyze Price Data:

### Objective:

1. Estimate the purchase price for any data in the past (Interpolate).
2. Extrapolate prices for one more year beyond the last available month-end point
3. Provide a function to input a date => output an estimated price

### Steps:

1. Interpolation:

   * Why? => Since the data provided is only monthly, in order to get the daily price, linear interpolation is used since it is defensible, simple and consistent. Interpolation for this case means that it assumes the best neutral guess for any date between 2 observed month-end prices is a straight line.
   * How? => use np.interp() but this only works with numbers and dates are not a number => use datetime64 to convert np.interp(x, xp, fp)

     * x: the estimated point (integer), xp: array of x values (integer), fp: array of y values
     * In this case: x is the date that needs to be estimated, xp is data\_int, fp is price\_vals



2. Extrapolation:

   * Why? => The current data ended in September 2024, while a contract might need the price in 2025, which is outside the provided data range. So there is a need to forecast future prices. 
   * One approach to this issue is to learn the trend and seasonality of the provided data. The following charts show prices gradually increasing over time (Trend) and prices rise in the winter, dip in the summer (Seasonality).
   * The trend and seasonality are clear, so the question now is how the model can understand them.

     * Seasonality is tricky since month numbers from 1 to 12 need to be put in a cycle => sin(2pi \* month / 12) and cos(2pi \* month / 12). Explain:

       * Since 1 to 12 are put in a cycle, they will be like a clock with 12 points on it. The use of the formula will identify the position of each point accordingly through its degree, and this will be understood by the regression model.
       * Both sin and cos are required because there is a need to differentiate different points as sin(30) = sin(150), which means January and May are at the same position, but cos(30) != cos(150). So, the (sin, cos) pair will give every month a unique coordinate.
     * Trend is simple since there is only one need to measure how many days have passed since the start => Use t as days since start. However, the trend doesn't increase in a straight line but rather increases at a changing rate => Add t^2 to represent such a curve.
   * In order to build the model, there needs to be a fixed start date (the earliest date in the dataset), calculate t, the angle and finally, combine t, t^2, sin, and cos.

     * t is the difference between the chosen date and the start date => .dt.days to get the number of day
     * month is just .dt.month of the chosen date
     * Both t and month need to be => .values.reshape() to turn into 2D array to be usable in np.interp()

### 

### Output:

<img width="392" height="278" alt="image" src="https://github.com/user-attachments/assets/ae59a239-492b-4e97-a17a-7cfad08cf5bc" />
<img width="382" height="278" alt="image" src="https://github.com/user-attachments/assets/6d4e6ccd-2fd7-4b50-b859-87decaaf3311" />
<img width="615" height="333" alt="image" src="https://github.com/user-attachments/assets/86ceeebd-7302-4d25-a12e-2a5d4020e633" />
<img width="727" height="387" alt="image" src="https://github.com/user-attachments/assets/8f41a141-936a-4b0c-91a3-f6c722b0cd17" />

## Contract Valuation:

### Context:

* Any trade agreement is as valuable as:
The price we can sell - The price we are able to buy - cost
* Profit <= Sell > Price + Cost
* Example: Purchase in summer at MMBtu $2/MMBtu and store for 4 months, and ensure to sell at $3/MMBtu, with $0.1 Storage cost per month, $0.01 injection/withdrawal cost per 1MMBtu and $0.05 transportation cost to and from facility.

=> Value of contract = (3-2) - 0.1\* 4 - 0.01 - 0.05\* 2 = 0.490 ($)

* Storage Trade Process:

  * Buy (Injection Date) => Outflow = Injected \* Buy Price
  * Store.
  * Sell (Withdrawal Date) => Inflow = Withdraw \* Sell Price

### Needed Inputs:

* Injection dates
* Withdrawal dates
* Volumes injected/withdrawn
* Injection and withdrawal rate limits
* Maximum storage capacity
* Storage cost (per month)
* Injection/withdrawal fees
* Transportation cost

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

