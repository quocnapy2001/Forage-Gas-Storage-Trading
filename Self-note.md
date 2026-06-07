

|Variable|Type|Describe|
|-|-|-|
|natgas\_df|DataFrame|Dates and Prices data|
|date\_int|integer|Data in numerical form (datetime64)|
|price\_vals|float|array of prices|





**PURPOSE:** Buy gas cheap in summer, store it, sell it expensive in winter => How much is such trade worth?



**DATA:**

* Monthly natural gas prices. Each data point is:

  * the market purchase price of natural gas.
  * for delivery at the end of that month.
  * from 31/10/2020 to 30/09/2024.





**INTERPOLATE:**

* Why? Since the data provided is only monthly so it order to get daily price, linear interpolation is used since it is defensible, simple and consistent Interpolation for this case mean that it assumed the  best neutral guess for any date between 2 observed month-end prices is a straight line.
* How? => use np.interp() 

  * but this only work with number and date is not number => use datetime64 to convert
  * np.interp(x, xp, fp)

    * x: the estimated point (integer), xp: array of x values (integer), fp: array of y values
    * In this case: x is the date that needed estimate, xp is data\_int, fp is price\_vals





**EXTRAPOLATE:**

**PRICING MODEL:**

