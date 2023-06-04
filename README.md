# Swastika_Portfolio_management

This Project Targets to compute multiple trading strategies parallely, this can be done efficiently through data sharing between different stratgies. The Strategy is a bit complicated to understand, therefore extensive details of the strategy has been given at the end.

This was a fullstack python project, which uses SWASTIKA Broker(for order execution) and Angel Broker(for data extraction)

> This has to be mentioned that there had been recent updates in angel broking API, and the changes has not been reflected in the code. Therefore make sure to make changes in the code according to new API design.


## Procedure To install this on your PC

 - Make Virtual env `virtualenv env`
 - Activate virtual enviroment `source env/bin/activate`
 - Install requirements. `pip3 install -r requirements.txt` or `pip install -r requirements.txt`
 - complete migrations through `python3 manage.py makemigrations` and `python3 manage.py migrate`
 - Run command to start the project `python3 manage.py runserver`


```
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```



### 1. Index page (main page)


![Alt text](https://github.com/sudhanshu8833/swastika_portfolio_management/blob/main/DOCUMNETS_ALGO/dashboard.png)


   - This should be accessible at `http://127.0.0.1:8000/data/index` if you are using local host
   - Angel Api keys, client id, password and token are provided and to be added within Code.
   - **Swastika credentials** has also to be added within the code.
   - **Multiplier** Here Multiplier represents the number of lots to be traded
   - Rest **ET,timeout, etc etc** are strategy specific therefore should try to understand through last section in strategy explanation
   - Here **start the strategy** button is going to start a new strategy for you
   - Here **data calulation** has to be clicked everyday before trading session begins



### 2. current positions page


![Alt text](https://github.com/sudhanshu8833/swastika_portfolio_management/blob/main/DOCUMNETS_ALGO/present_position.png)

  - available at `http://127.0.0.1:8000/data/position/` if you are running on local hosts
  - Details about all the open strategies are mentioned here.
  - The fields are more or less self explanatory



### 3. order history page


  - available at `http://127.0.0.1:8000/data/order` on local host.
  - Details about all the Closed strategies are mentioned here.
  - The fields are more or less self explanatory.
  - A lot of additional Info's are also provided to analyze the day.


## STRATEGY EXPLANATION


### Admin Panel parameters

| PARTICULAR | DESCRIPTION | DEFAULT | TYPE             |
|------------|-------------|---------|------------------|
| BF         | BUY FACTOR  | 300     | WHOLE NUMBER     |
| A          | % PREMIUM   | 0.99    | FRACTION (FLOAT: 0 TO 1) |
| t          | TIME        | 60      | SECONDS          |
| TP1        | %           | 40      | NUMBER           |
| TP2        | %           | 90      | NUMBER           |


### Details about Different Conditions that can arise in the market

| Trigger Point | Condition                                             | Action                                 |
| ------------- | ----------------------------------------------------- | -------------------------------------- |
| T1            | Nifty level <= Spot nifty - (V * TP2)                  | Square Off all trades                  |
| T2            | Nifty level <= Spot nifty - ((V - sellfactor) * TP1)  | STRATEGY EXIT                          |
| T3            | Nifty level = Spot nifty                               | Square off all sell trades             |
| T4            | Nifty level >= Spot nifty + ((V - sell factor) * TP1) | S = new spot nifty<br>CE S- strategy<br>PE S+ strategy |
| T5            | Nifty level >= Spot nifty + (V * TP2)                  | If T2/T4 is already triggered<br>Then sell pair restored to original sell pair |
| T6            | If P3/P4 < ET (ET is manually entered by admin, default 50) | Square off all sell trades and create new sell pair at new spot nifty<br>S = new spot nifty<br>CE S- strategy<br>PE S+ strategy |
| T7            | Manual exit button                                    | Square Off all trades<br>Select desired set of pair and square off |


The table represents different trigger points (T1, T2, T3, etc.) along with their corresponding conditions and actions in a trading strategy. Here's an explanation of each row:

T1: This trigger occurs when the Nifty level is less than or equal to the Spot Nifty minus (V multiplied by TP2). The action associated with this trigger is to square off all trades.

T2: This trigger occurs when the Nifty level is less than or equal to the Spot Nifty minus ((V minus sellfactor) multiplied by TP1). The action associated with this trigger is to exit the strategy.

T3: This trigger occurs when the Nifty level is equal to the Spot Nifty. The action associated with this trigger is to square off all sell trades.

T4: This trigger occurs when the Nifty level is greater than or equal to the Spot Nifty plus ((V minus sell factor) multiplied by TP1). The actions associated with this trigger are: set S as the new spot nifty, execute CE S- strategy, and execute PE S+ strategy.

T5: This trigger occurs when the Nifty level is greater than or equal to the Spot Nifty plus (V multiplied by TP2). If T2 or T4 is already triggered, the sell pair is restored to the original sell pair.

T6: This trigger occurs when P3 divided by P4 is less than the ET value (manually entered by the admin, default 50). The actions associated with this trigger are: square off all sell trades, create a new sell pair at the new spot nifty (S), execute CE S- strategy, and execute PE S+ strategy.

T7: This trigger represents a manual exit button. The action associated with this trigger is to square off all trades. Additionally, the user can select a desired set of pairs and square them off.


### Table Heading: Current Market Data

| DATE               | CURRENT DATE       | INDEX                 |
|--------------------|--------------------|-----------------------|
| TIME               | CURRENT TIME       | THROUGH API           |
| NIFTY              | CURRENT NIFTY      | THROUGH CALCULATION   |
| SPOT NIFTY LVL (N) | THROUGH CALCULATIONS | DROP DOWN LIST       |
| VIX                | CURRENT VIX        | VARIABLES             |
| EXPIRY             | EXPIRY DATE        |                       |
| SELL PAIR FACTOR (SF) | DROP DOWN LIST{0,50,100} |                    |
| MULTIPLICATION (M) | DROP DOWN LIST (0,1,2 - 100) |                    |

DATE: This column represents the date, and "CURRENT DATE" refers to the current date.

TIME: This column represents the time, and "CURRENT TIME" refers to the current time obtained through an API.

INDEX: This column refers to a specific market index, which is not specified in the provided information. It could represent a stock index like the S&P 500 or any other relevant financial index.

NIFTY: This column represents the NIFTY index. "CURRENT NIFTY" refers to the current value of the NIFTY index, obtained through calculations.

SPOT NIFTY LVL (N): This column represents the spot level of the NIFTY index. The value is obtained through calculations.

VIX: This column represents the VIX index, which is a measure of market volatility. "CURRENT VIX" refers to the current value of the VIX index.

EXPIRY: This column represents the expiry date, which is not specified in the provided information.

SELL PAIR FACTOR (SF): This column represents a factor for selling pairs, with options in the drop-down list being {0, 50, 100}.

MULTIPLICATION (M): This column represents a multiplication factor, with options in the drop-down list being (0, 1, 2 - 100).

Please note that some information, such as the specific market index and expiry date, is not provided in the given table.





### BUY PAIR

| EXPIRY       | STRIKE | OPTION TYPE | PREMIUM | LOTS |
|--------------|--------|-------------|---------|------|
| EXPIRY DATE  | N-V    | CE          | P1      | M*1  |
| EXPIRY DATE  | N+V    | PE          | P2      | M*1  |
|              |        | P1 + P2     |         |      |

### SELL PAIR
| EXPIRY       | STRIKE | OPTION TYPE | PREMIUM | LOTS |
|--------------|--------|-------------|---------|------|
| EXPIRY DATE  | N-SF   | CE          | P3      | M*1  |
| EXPIRY DATE  | N+SF   | PE          | P4      | M*1  |
|              |        | P3 + P4     |         |      |

EXPIRY: This column represents the expiry date of the options.

STRIKE: This column represents the strike price of the options.

OPTION TYPE: This column represents the type of options (Call Option: CE, Put Option: PE).

PREMIUM: This column represents the premium (price) of the options.

LOTS: This column represents the number of lots for the options, which is calculated as M*1.



##### Table Heading: Trading Strategy Parameters



| PARTICULAR         | DESCRIPTION                                          | CALCULATION                                | SOURCE |
|--------------------|------------------------------------------------------|--------------------------------------------|--------|
| CURRENT NIFTY      | NSE DERIVATIVE INDEX                                 |                                            | API    |
| CURRENT VIX        | NSE DERIVATIVE INDEX FOR VOLATILITY                   |                                            | API    |
| CURRENT DATE       | LIVE MARKET DATE                                     |                                            | API    |
| CURRENT TIME       | LIVE MARKET TIME                                     |                                            | API    |
| P1, P2, P3, P4     | PREMIUM FROM API                                     | ACC TO STRIKE, EXPIRY, OPTION TYPE          | API    |
| SPOT NIFTY LVL(N)  | NEAREST 50 ROUND OF NIFTY LVL                        | ROUND(NIFTYLVL/50,0)*50                     | CALCULATION |
| V                  | BUY FACTOR                                           | CALCULATE ACCORDING TO VOLATILITY TABLE     | CALCULATION |
| WORKING DAYS (d)   | NO OF MARKET DAYS TO TRADE EXPIRY                    | EXPIRY DATE - CURRENT DATE - HOLIDAYS IN BETWEEN | CALCULATION |
| SELL PAIR FACTOR(SF) | FACTORS TO DECIDE SELL STRIKE PRICE                 | SELECTED MANUALLY                          | MANUALLY |
| MULTIPLICATION     | NO OF LOTS OF EACH LEG TO BE TRADED                   | SELECTED MANUALLY                          | MANUALLY |
| EXPIRY DATE        | ON THE DATE AT WHICH INSTRUMENT EXPIRES               | BY DEFAULT IS CURRENT WEEK BUT IF V IS <(BF) (e.g.: 300) THAN NEXT WEEK | MANUALLY |
| BF                 | DEFAULT BUY FACTOR                                   | ADMIN PARAMETER (DEFAULT: 300)              | ADMIN  |
| START              | START CALCULATIONS IN STRATEGY ACC TO SELECTED PARAMETERS | NA                                       | NA     |

CURRENT NIFTY: Represents the current value of the NSE derivative index. The value is obtained from an API.

CURRENT VIX: Represents the current value of the NSE derivative index for volatility. The value is obtained from an API.

CURRENT DATE: Represents the current date of the live market. The value is obtained from an API.

CURRENT TIME: Represents the current time of the live market. The value is obtained from an API.

P1, P2, P3, P4: Represents the premiums of different options contracts. The values are obtained from an API and calculated based on the 
strike price, expiry date, and option type.

SPOT NIFTY LVL(N): Represents the nearest round figure of the NIFTY level. It is calculated as ROUND(NIFTYLVL/50,0)*50, where NIFTYLVL represents the NIFTY level.

V: Represents the buy factor calculated based on a volatility table.

WORKING DAYS (d): Represents the number of market days to trade expiry. It is calculated as the difference between the expiry date, current date, and the holidays in between.

SELL PAIR FACTOR (SF): Represents the factors used to decide the sell strike price. It is selected manually.

MULTIPLICATION: Represents the number of lots of each leg to be traded. It is selected manually.

EXPIRY DATE: Represents the date on which the instrument expires. By default, it is set to the current week, but if V is less than the default buy factor (BF), it is set to the next week. It is determined manually


### Example for volatility table 

| VIX | NIFTY | WORKING DAYS (d) | DAYS VIX | NIFTY RANGE | V FACTOR |
|-----|-------|-----------------|----------|-------------|----------|
| 21  | 15850 | 1               | 1.32     | 166         | 150      |
| 21  | 15850 | 2               | 1.87     | 234         | 250      |
| 21  | 15850 | 3               | 2.29     | 287         | 300      |
| 21  | 15850 | 4               | 2.65     | 331         | 350      |
| 21  | 15850 | 5               | 2.96     | 370         | 350      |
| 21  | 15850 | 6               | 3.24     | 406         | 400      |
| 21  | 15850 | 7               | 3.50     | 438         | 450      |
| 21  | 15850 | 8               | 3.74     | 469         | 450      |
| 21  | 15850 | 9               | 3.97     | 497         | 500      |
| 21  | 15850 | 10              | 4.18     | 524         | 500      |
| 21  | 15850 | 11              | 4.39     | 549         | 550      |
| 21  | 15850 | 12              | 4.58     | 574         | 550      |



### Table Heading: Trading Strategy Parameters and Calculations


| DATE         | CURRENT DATE  | MAX EARNING ON EXPIRY (E) | E                   |
|--------------|---------------|--------------------------|---------------------|
| TIME         | CURRENT TIME  | MAX RISK ON EXPIRY (R)    | R                   |
| NIFTY        | CURRENT NIFTY | E/R                      | E/R                 |
| VIX          | CURRENT VIX   | MARGIN                    | API                 |
| EXPIRY       | EXPIRY DATE   | TOTAL FUND NEEDED         | CALC                |
|              |               |                          |                     |
| BUY PAIR     |               | TRADE TYPE                | LIMIT               |
| EXPIRY       | STRIKE        | OPTION TYPE               | PREMIUM             |
| EXPIRY DATE  | N-V           | CE                        | P1                  |
| EXPIRY DATE  | N+V           | PE                        | P2                  |
|              |               | P1 + P2                   |                     |
|              |               |                          |                     |
| SELL PAIR    |               | EXECUTE                   |                     |
| EXPIRY       | STRIKE        | OPTION TYPE               | PREMIUM             |
| EXPIRY DATE  | N-SF          | CE                        | P3                  |
| EXPIRY DATE  | N+SF          | PE                        | P4                  |
|              |               | P3 + P4                   |                     |

The table includes various parameters and calculations for a trading strategy. Here's an explanation of each section:

Date Section:

CURRENT DATE: Represents the current date in the live market.

MAX EARNING ON EXPIRY (E): Placeholder for the maximum earning potential on expiry.

E: Placeholder for the actual value of the maximum earning potential on expiry.



Time Section:

CURRENT TIME: Represents the current time in the live market.

MAX RISK ON EXPIRY (R): Placeholder for the maximum risk on expiry.

R: Placeholder for the actual value of the maximum risk on expiry.


NIFTY Section:

CURRENT NIFTY: Represents the current value of the NSE derivative index.

E/R: Placeholder for the ratio of maximum earning potential to maximum risk.


VIX Section:

CURRENT VIX: Represents the current value of the NSE derivative index for volatility.

MARGIN: Placeholder for the margin required for trading. The value is obtained from an API.


Expiry Section:

EXPIRY DATE: Represents the expiry date of the trading instrument.

TOTAL FUND NEEDED: Placeholder for the total fund required for trading. The actual value is calculated.


Buy Pair Section:

TRADE TYPE: Placeholder for the type of trade.

LIMIT: Placeholder for the limit of the trade.

EXPIRY: Represents the expiry date of the options contract.

STRIKE: Represents the strike price of the options contract.

OPTION TYPE: Represents the type of the options contract (CE or PE).

PREMIUM: Represents the premium of the options contract.


Sell Pair Section:

EXECUTE: Placeholder for the execution of the trade.

EXPIRY: Represents the expiry date of the options contract.

STRIKE: Represents the strike price of the options contract.

OPTION TYPE: Represents the type of the options contract (CE or PE).

PREMIUM: Represents the premium of the options contract.

Please note that the table provided contains placeholders for calculations and actual values. The specific calculations and values need to be filled in based on the trading strategy and its implementation.




### Strategy Build Sheet - Notes

| PARTICULAR       | DESCRIPTION                                    | CALCULATION                              | SOURCE |
|------------------|------------------------------------------------|------------------------------------------|--------|
| E                | EARNING AT EXPIRY                              | {(P3+P4-2*SF)-(P1+P2-2*V)}*M*50          | CALC   |
| R                | RISK AT EXPIRY                                 | (V-SF)*M*50 - E                          | CALC   |
| E/R              | RATIO OF EARNING TO RISK AT EXPIRY              | E/R                                      | CALC   |
| MARGIN           | MARGIN NEEDED FOR PAIR                          | FROM API                                 | API    |
| TOTAL FUND NEEDED | TOTAL FUND NEEDED FOR TRADE                     | MARGIN + (P1+P2-P3-P4)*50                | CALC   |
| TRADE TYPE       | HOW THE STRATEGY IS EXECUTED                    | 1) MARKET     2) LIMIT                   | MANUAL |
| MARKET           | ALL TRADES EXECUTED AT MARKET RATES             | OPTION 1                                 | NA     |
| LIMIT            | RATE SET ACCORDING TO ADMIN CALCULATION         | AND TRIGGERS TRADE IF CONDITIONS ARE MET | NA     |
| PT1              | PREMIUM TRIGGER 1                              | P1*A                                     | CALC   |
| PT2              | PREMIUM TRIGGER 2                              | P2*A                                     | CALC   |
| A                | ADMIN PARAMETER                                | FRACTION (0 TO .99){DEFAULT: .99}        | ADMIN  |
| t                | ADMIN PARAMETER                                | IN SECONDS (DEFAULT: 60)                 | ADMIN  |
| EXECUTE          | TRIGGER FOR TRADE EXECUTION                     | NA                                       | NA     |

The table represents various notes and calculations related to the strategy build sheet. Here's an explanation of each section:

Particular Section:

PARTICULAR: Represents the specific parameter or calculation.
DESCRIPTION: Provides a description of the particular parameter or calculation.
CALCULATION: Describes the formula or method used for calculation.
SOURCE: Indicates the source of the data or information.
E Section:

E: Represents the earnings at expiry.
EARNING AT EXPIRY: Placeholder for the calculation of earnings at expiry.
{(P3+P4-2SF)-(P1+P2-2V)}M50: Placeholder for the actual calculation of earnings at expiry.
R Section:

R: Represents the risk at expiry.
RISK AT EXPIRY: Placeholder for the calculation of risk at expiry.
(V-SF)M50 - E: Placeholder for the actual calculation of risk at expiry.
E/R Section:

E/R: Represents the ratio of earnings to risk at expiry.
RATIO OF EARNING TO RISK AT EXPIRY: Placeholder for the calculation of the E/R ratio.
E/R: Placeholder for the actual E/R ratio.
Margin Section:

MARGIN: Represents the margin needed for the trading pair.
MARGIN NEEDED FOR PAIR: Placeholder for obtaining the margin from an API.
Total Fund Needed Section:

TOTAL FUND NEEDED: Represents the total fund needed for the trade.
TOTAL FUND NEEDED FOR TRADE: Placeholder for the calculation of the total fund needed.
MARGIN + (P1+P2-P3-P4)*50: Placeholder for the actual calculation of the total fund needed.
Trade Type Section:

TRADE TYPE: Represents how the strategy is executed.
HOW THE STRATEGY IS EXECUTED: Placeholder for selecting the trade type (Market or Limit).
MARKET: Placeholder for executing all trades at market rates.
LIMIT: Placeholder for setting the rate according to admin calculation and triggering trade if conditions are met.
PT1 and PT2 Sections:

PT1: Represents the premium trigger 1.
PT2: Represents the premium trigger 2.
PREMIUM TRIGGER 1: Placeholder for the calculation of the premium trigger 1.
PREMIUM TRIGGER 2: Placeholder for the calculation of the premium trigger 2.
P1A and P2A: Placeholders for the actual calculations of the premium triggers, with A representing the admin parameter.
A and t Sections:

A: Represents the admin parameter.
t: Represents the admin parameter.
ADMIN PARAMETER: Placeholder for the admin parameter values.
FRACTION (0 TO .99){DEFAULT: .99}: Placeholder for the actual value of the admin parameter.
IN SECONDS (DEFAULT: 60): Placeholder for the default value of the admin parameter.
EXECUTE Section:

EXECUTE: Represents the trigger for trade execution.
TRIGGER FOR TRADE EXECUTION: Placeholder indicating the trigger for trade execution.
Please note that the table provided contains placeholders for calculations and actual values. The specific calculations and values need to be filled in based on the trading strategy and its implementation.


