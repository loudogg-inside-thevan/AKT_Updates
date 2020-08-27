# AKT_Updates

AKT stands for Analyst Key Takeaways (AKT). I am a mutual fund analyst who on a quarterly basis scores my company's coverage universe of funds on 6 metrics: Risk-Return Profile, Tenure, Volatility Profile, Fees (relative to mutual fund peers), Performance (relative to mutual fund peers), Equity Correlation, and Fixed Income Correlation. The responses are standardized and quantitatively defined, thus I built this project to automate a part of the process for producing the quarterly metric responses for input into our database.

The first component to this program is Share_Class.py. It takes an export of data from our proprietary database saved as a csv filed titled 'y - Share Classes.csv' and produces an excel file of tickers. Tickers are 5 letter symbols used to identify mutual funds by there share class (each fund will have anywhere from 2 to 6+ share classes). The AKTs are entered by fund, and thus, for each fund we must identify the share class used to 'score' the 6 metrics. That is what Share_Class.py does, it provides a list of the selected share classes by there ticker to be used in the AKT process. The share classes are chosen by the following rules which have been built into the Share_Class.py program:

"The share class used for the Analyst Key Takeaways section is the share class with the longest track record and a share class type of 1) Fee Based, 2) A Share, and 3)     Institutional (in order of preference based on availability)."

