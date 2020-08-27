# Lucas Johnson
# The program leverages two csv file imports and user defined variables to define responses used as input data for the
# AKT process.

import pandas as pd
import openpyxl
import csv

# Create a dataframe of the parameter data from the excel spreadsheet. The parameter csv file contains data that is
# used to define Fees and Performance inputs below.
param_df = pd.read_csv('y - Parameters.csv')                                           # file import
param_df.set_index('Identifier', inplace=True)

# Establish variables for the parameters used to create the AKT inputs. These must be updated by the user each quarter
# when the process is performed.
down_beta = 0.45
equity_vol_low = 0.1634
equity_vol_high = 0.1734
fi_vol_low = 0.0288
fi_vol_high = 0.0388
neg_corr = -0.1
none_corr = 0.1
low_corr = 0.3
mod_corr = 0.5

# Create a dataframe of the fund data for iteration. The fund data csv file contains data exported from our proprietary
# database that will be used in addition to the 'parameters' file to establish responses for the AKT process.
df_2 = pd.read_csv('y - Fund Data.csv')                                                     # file import

# Creates and writes a csv file with the respective AKT input responses for each fund (line item) in df_2.
with open('z - AKT Data', 'w', newline='') as csvfile:

    # Writes the column headers for the csv file.
    akt_writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    akt_writer.writerow(['Fund Name', 'Ticker', 'Risk-Ret Profile', 'Tenure', 'Vol Profile', 'Fees', 'Performance',
                         'Eq Corr', 'FI Corr'])

    # Works through each fund to define the input responses saved as variables for the AKT process.
    for row in df_2.itertuples():

        # Creates variables to hold the fund indentification data for the AKT responses.
        fund_name = row[1]
        ticker = row[2]

        # Creates variables to hold the AKT input data for each fund.
        risk_ret = None
        tenure = None
        vol = None
        fees = None
        perform = None
        eq_corr = None
        fi_corr = None

    # Risk-return profile variable set.
        if row[6] < down_beta and row[7] < down_beta:
            risk_ret = 'Core Alternative'
        if row[6] < down_beta and row[7] >= down_beta:
            risk_ret = 'Alternative FI'
        if row[6] >= down_beta and row[7] < down_beta:
            risk_ret = 'Alternative Equity'
        if row[6] >= down_beta and row[7] >= down_beta:
            risk_ret = 'Alternative Beta'

    # Tenure variable set.
        if row[11] >= 120:
            tenure = 'Greater - 10'
        if row[11] >= 60 and row[11] < 120:
            tenure = 'Greater - 5'
        if row[11] >= 36 and row[11] < 60:
            tenure = 'Greater - 3'
        if row[11] < 36:
            tenure = 'Less - 3'

    # Volatility profile variable set.
        if row[10] > equity_vol_high:
            vol = 'Greater - Equity'
        if row[10] <= equity_vol_high and row[10] >= equity_vol_low:
            vol = 'Comparable - Equity'
        if row[10] < equity_vol_low and row[10] > fi_vol_high:
            vol = 'Inbetween'
        if row[10] <= fi_vol_high and row[10] >= fi_vol_low:
            vol = 'Comparable - FI'
        if row[10] < fi_vol_low:
            vol = 'Less - FI'

    # Fees variable set.
        if row[4] > param_df.loc[row[3], 'Fee High']:
            fees = 'Above'
        if row[4] <= param_df.loc[row[3], 'Fee High'] and row[4] >= param_df.loc[row[3], 'Fee Low']:
            fees = 'Comparable'
        if row[4] < param_df.loc[row[3], 'Fee Low']:
            fees = 'Below'

    # Performance variable set.
        if row[5] > param_df.loc[row[3], '3 High']:
            perform = 'Above'
        if row[5] <= param_df.loc[row[3], '3 High'] and row[5] >= param_df.loc[row[3], '3 Low']:
            perform = 'Comparable'
        if row[5] < param_df.loc[row[3], '3 Low']:
            perform = 'Below'

    # Equity Correlation variable set.
        if row[8] < neg_corr:
            eq_corr = 'Negative'
        if row[8] >= neg_corr and row[8] < none_corr:
            eq_corr = 'None'
        if row[8] >= none_corr and row[8] < low_corr:
            eq_corr = 'Low'
        if row[8] >= low_corr and row[8] < mod_corr:
            eq_corr = 'Moderate'
        if row[8] >= mod_corr:
            eq_corr = 'High'

    # Fixed Income Correlation variable set.
        if row[9] < neg_corr:
            fi_corr = 'Negative'
        if row[9] >= neg_corr and row[9] < none_corr:
            fi_corr = 'None'
        if row[9] >= none_corr and row[9] < low_corr:
            fi_corr = 'Low'
        if row[9] >= low_corr and row[9] < mod_corr:
            fi_corr = 'Moderate'
        if row[9] >= mod_corr:
            fi_corr = 'High'

        # Takes the fund identification variables and AKT input variables and writes them into the csv file for the
        # fund in question.
        akt_writer.writerow([fund_name, ticker, risk_ret, tenure, vol, fees, perform, eq_corr, fi_corr])

# Reads the newly written AKT data csv file and writes it into an excel file.
read_file = pd.read_csv(r'C:\Users\ljohnson\PycharmProjects\AKT_Updates\z - AKT Data')
read_file.to_excel(r'C:\Users\ljohnson\PycharmProjects\AKT_Updates\z - AKT Input Data.xlsx', index=None, header=True)
