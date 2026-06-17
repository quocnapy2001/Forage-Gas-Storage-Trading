# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 12:47:51 2026

@author: Owner
"""

from data_0 import pd
from extrapolation_2 import estimate_gas_price

### Pricing Function (Excluding transportation dealy, 0 int, 0 holidays)
def price_storage_contract(
        inj_dates,
        wdr_dates,
        inj_vol,
        wdr_vol,
        inj_rate,
        wdr_rate,
        max_vol,
        storage_cost,           # Per Month
        inj_cost = 0.0,         # Per Unit  
        wdr_cost = 0.0,         # Per Unit
        transport_cost = 0.0    # Per Event
        ):
    
    """
    Prices a gas storage contract using inventory-based cash flow modelling.
    Assumes:
    - Zero interest rate
    - No transport delay
    - No holidays
    """
    
    inj_dates = pd.to_datetime(inj_dates).to_list()
    wdr_dates = pd.to_datetime(wdr_dates).to_list()
    
    events = []
    for d in inj_dates:
        events.append(("inject", d))
    for d in wdr_dates:
        events.append(("withdraw", d))
        
    events.sort(key=lambda x: x[1])
    
    storage_level = 0.0
    contract_val = 0.0
    last_event_date = None
    
    event_log = []
    
    # Month approximation
    def months_between(d1,d2):
        return (d2.year - d1.year) * 12 + (d2.month - d1.month)
    
    # Events process
    for event_type, event_date in events:
        
        buy_price = None
        sell_price = None
        
        # Storage cost 
        months_passed = 0
        if last_event_date is not None:
            months_passed = months_between(last_event_date, event_date)
            contract_val -= storage_cost * months_passed
        
            
        # Injection Process
        if event_type == "inject":
            # Constraints
            if inj_vol > inj_rate:
                raise ValueError("Injection Rate Exceeded.")
            if storage_level + inj_vol > max_vol:
                raise ValueError("Maximum Capacity Exceeded.")
            
            # Value
            buy_price =  estimate_gas_price(event_date)
            
            total_inj_cost = (buy_price + inj_cost) * inj_vol
            total_cost   = total_inj_cost + transport_cost
            contract_val -= total_cost
            
            # Increase Storage Level
            storage_level += inj_vol
            
        # Withdrawal Process
        elif event_type == "withdraw":
            # Constraints
            if wdr_vol > wdr_rate:
                raise ValueError("Withdrawal Rate Exceeded.")
            if wdr_vol > storage_level:
                raise ValueError("Mininum Capacity Exceeded.")
                
            # Value
            sell_price =  estimate_gas_price(event_date)
            
            rev_from_withdraw = (sell_price - wdr_cost) * wdr_vol
            total_rev = rev_from_withdraw - transport_cost
            contract_val += total_rev
            
            # Decrease Storage Level
            storage_level -= wdr_vol
        
        event_log.append({
            "date": event_date.strftime("%Y-%m-%d"),
            "type": event_type,
            "Months charged": months_passed,
            "Storage cost": f"£{storage_cost * months_passed:,.2f}",
            "Transport cost": f"£{transport_cost:,.2f}",
            "Buy price": f"£{buy_price:,.2f}" if buy_price is not None else "",
            "Sell price": f"£{sell_price:,.2f}" if sell_price is not None else "",
            "Storage level": f"{storage_level:,.0f}",
            "Contract value": f"£{contract_val:,.2f}"
        })
            
        last_event_date = event_date
        
    return contract_val, pd.DataFrame(event_log)
    
val, event_df = price_storage_contract(
                inj_dates=["2024-10-31","2024-12-31"],
                wdr_dates=["2025-02-28"],
                inj_vol=1_000_000,
                wdr_vol=2_000_000,
                inj_rate=2_000_000,
                wdr_rate=2_000_000,
                max_vol=2_000_000,
                storage_cost=100_000,           
                inj_cost = 0.01,           
                wdr_cost = 0.01,        
                transport_cost = 50_000   
                )

print(val)