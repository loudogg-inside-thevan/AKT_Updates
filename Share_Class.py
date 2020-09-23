# Author: Lucas Johnson
# Description: Reads a csv file of AI Insight alternative mutual funds that includes share class information as column
# data points and returns a csv file of the selected share class for each fund for the 'analyst key takeaways' (AKT)
# process.

import pandas as pd
import pprint
import openpyxl

file = "C:\\Users\\ljohnson\\PycharmProjects\\AKT_Updates\\Input Sheets\\y - Share Classes.csv"
share_data = pd.read_csv(file)

# Creates a dictionary composed of each fund and whose value is equal to a dictionary of the fund's share classes. The
# value of each share class is also equal to a dictionary with kay-value pairs for class, ticker, and tenure data points.

share_dict = {}

for row in share_data.itertuples():

    # If the fund key is already within the dictionary, then a new value dictionary is created within the fund key for
    # the share class and its respective data for class, ticker, and tenure.
    if row[1] in share_dict:
         share_dict[row[1]][row[2]] = {}
         share_dict[row[1]][row[2]]['Ticker'] = row[3]
         share_dict[row[1]][row[2]]['Tenure'] = row[5]
         share_dict[row[1]][row[2]]['Type'] = row[4]

    # If the fund is not a key within the dictionary, a key is created for the fund and a dictionary is created as its
    # key value for the share class and its respective data for class, ticker, and tenure.
    else:
        share_dict[row[1]] = {}
        share_dict[row[1]][row[2]] = {}
        share_dict[row[1]][row[2]]['Ticker'] = row[3]
        share_dict[row[1]][row[2]]['Tenure'] = row[5]
        share_dict[row[1]][row[2]]['Type'] = row[4]

# Creates a new dictionary from the original share_dict that removes any share class for each fund whose tenure is less
# than the funds longest tenured share class.

tenure_dict = {}

for fund in share_dict:

    # Loops through each share class dictionary for each fund to establish what the max tenure is for each fund
    # excluding the C Share and Retirement share class types.
    max_tenure = 0
    for share in share_dict[fund]:
        if share_dict[fund][share]['Tenure'] > max_tenure and share_dict[fund][share]['Type'] != 'C Share' and\
                share_dict[fund][share]['Type'] != 'Retirement':
            max_tenure = share_dict[fund][share]['Tenure']

    # remove share classes whose tenure is below the max tenure
    for share in share_dict[fund]:
        if share_dict[fund][share]['Tenure'] == max_tenure:
            if fund in tenure_dict:
                tenure_dict[fund][share] = share_dict[fund][share]
            else:
                tenure_dict[fund] = {}
                tenure_dict[fund][share] = {}
                tenure_dict[fund][share] = share_dict[fund][share]

# Creates a new dictionary from the tenure_dict that includes each fund and the share class that should be used
# for AKT.

AKT_dict = {}

for fund in tenure_dict:

    # Creates a list of the share class "types" for the fund in tenure_dict in question.
    type_list = []

    for share in tenure_dict[fund]:
        type_list.append(tenure_dict[fund][share]['Type'])

    # Established dummy variables for the 3 share class types in question for the next part of this program. These
    # include Fee Based, A Share, and Institutional.
    fee_type = False
    a_type = False
    inst_type = False

    # Adjusts the dummy variable to True if the share "type" in question is within the list.
    if "Fee Based" in type_list:
        fee_type = True

    if "A Share" in type_list:
        a_type = True

    if "Institutional" in type_list:
        inst_type = True

    # The default (desired) share class for the AKT process is Fee Based. If True, it adds the the fund and share class
    # data into the AKT_dict.
    if fee_type == True:

        for share in tenure_dict[fund]:

            if tenure_dict[fund][share]['Type'] == "Fee Based":
                if fund in AKT_dict:
                    AKT_dict[fund][share] = tenure_dict[fund][share]
                else:
                    AKT_dict[fund] = {}
                    AKT_dict[fund][share] = {}
                    AKT_dict[fund][share] = tenure_dict[fund][share]

    # The second default (desired) share class for the AKT process is A Share. If True and there is no Fee Based, it
    # adds the the fund and share class data into the AKT_dict.
    if fee_type == False and a_type == True:

        for share in tenure_dict[fund]:

            if tenure_dict[fund][share]['Type'] == "A Share":
                if fund in AKT_dict:
                    AKT_dict[fund][share] = tenure_dict[fund][share]
                else:
                    AKT_dict[fund] = {}
                    AKT_dict[fund][share] = {}
                    AKT_dict[fund][share] = tenure_dict[fund][share]

    # The third default (desired) share class for the AKT process is Institutional. If True and there is no Fee Based or
    # A Share, it adds the the fund and share class data into the AKT_dict.
    if fee_type == False and a_type == False and inst_type == True:

        for share in tenure_dict[fund]:

            if tenure_dict[fund][share]['Type'] == "Institutional":
                if fund in AKT_dict:
                    AKT_dict[fund][share] = tenure_dict[fund][share]
                else:
                    AKT_dict[fund] = {}
                    AKT_dict[fund][share] = {}
                    AKT_dict[fund][share] = tenure_dict[fund][share]

# Creates a list of all tickers within the AKT_dict.
ticker_list = []

for fund in AKT_dict:
    for share in AKT_dict[fund]:
        ticker_list.append(AKT_dict[fund][share]['Ticker'])

# Converts the ticker list into a dataframe.
ticker_df = pd.DataFrame(ticker_list,columns=['AKT Tickers'])

# writes the ticker dataframe to an excel file within an output folder of the pycharm project

out_path = "C:\\Users\\ljohnson\\PycharmProjects\\AKT_Updates\\Output Sheets\\AKT Tickers.xlsx"
writer = pd.ExcelWriter(out_path, engine='openpyxl')
ticker_df.to_excel(writer, sheet_name="AKT Tickers")
writer.save()
