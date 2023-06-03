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



1. **Index page (main page)**


![Alt text](https://github.com/sudhanshu8833/Options-Trading-Bot-Angel-Broking-/blob/main/dashboard.png)


   - This should be accessible at `http://127.0.0.1:8000/data/index` if you are using local host
   - Angel Api keys, client id, password and token are provided and to be added within Code.
   - **Swastika credentials** has also to be added within the code.
   - **Multiplier** Here Multiplier represents the number of lots to be traded
   - Rest **ET,timeout, etc etc** are strategy specific therefore should try to understand through last section in strategy explanation
   - Here **start the strategy** button is going to start a new strategy for you
   - Here **data calulation** has to be clicked everyday before trading session begins



2. **current positions page**


![Alt text](https://github.com/sudhanshu8833/Options-Trading-Bot-Angel-Broking-/blob/main/positions.png)

  - available at `http://127.0.0.1:8000/data/position/` if you are running on local hosts
  - Details about all the open strategies are mentioned here.
  - The fields are more or less self explanatory



3. **order history page**


  - available at `http://127.0.0.1:8000/data/order` on local host.
  - Details about all the Closed strategies are mentioned here.
  - The fields are more or less self explanatory.
  - A lot of additional Info's are also provided to analyze the day.


## STRATEGY EXPLANATION

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

### Index Info

| DATE               | CURRENT DATE       | INDEX                 |
|--------------------|--------------------|-----------------------|
| TIME               | CURRENT TIME       | THROUGH API           |
| NIFTY              | CURRENT NIFTY      | THROUGH CALCULATION   |
| SPOT NIFTY LVL (N) | THROUGH CALCULATIONS | DROP DOWN LIST       |
| VIX                | CURRENT VIX        | VARIABLES             |
| EXPIRY             | EXPIRY DATE        |                       |
| SELL PAIR FACTOR (SF) | DROP DOWN LIST{0,50,100} |                    |
| MULTIPLICATION (M) | DROP DOWN LIST (0,1,2 - 100) |                    |



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

### strategy explanation


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



### Actual Strategy Table


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

### Admin Panel parameters

| PARTICULAR | DESCRIPTION | DEFAULT | TYPE             |
|------------|-------------|---------|------------------|
| BF         | BUY FACTOR  | 300     | WHOLE NUMBER     |
| A          | % PREMIUM   | 0.99    | FRACTION (FLOAT: 0 TO 1) |
| t          | TIME        | 60      | SECONDS          |
| TP1        | %           | 40      | NUMBER           |
| TP2        | %           | 90      | NUMBER           |
