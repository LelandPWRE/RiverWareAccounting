#Import packages here:
import os
import re
import csv
from pandas import *

"""
Overview
Purpose: Automate adding accounts to RiverWare
Python: version 3.8.1
Author: Leland Dorchester
"""

# TODO: Count number of accounts in model, and count number of accounts in new accounts file. Make a comparison
            # We need to know how many accounts need to be deleted, and how many accounts needs to be added.
# TODO: We probably need to know how many accounts are on each object, and how many accounts we would like to add/remove from each object.
# TODO: add a changelog that illustrates object by object, which accounts were added, removed, or changed. 
# Can we create a dictionary of existing accounts, a dictionary of accounts we need to add, then perform a comparison to create the changelog?

def CheckEveryAccountToRemoveExists(f,f2,WRData):
    # This functions searches for every account listed in the AccountsToRemove dataframe in the model text file
    # if the account is found, a counter is updated. The end result of the count of accounts found, must be the
    # same length as the accounts planned to remove. If these lengths don't match, the mapping wont work, so we 
    # exit the python script
    DFOfAcctsToRemove = WRData['AccountsToRemove']
    ata = len(WRData['AccountsToAdd'])
    atr = len(WRData['AccountsToRemove'])
    rowctr = 0
    FoundAccts = 0
    for x in f: # loop through each line in the file

        # check if   "$obj acct dive"   is contained in the string
        if "\"$obj\" acct dive" in x:
            print('row: ', rowctr, '\n')

            for AcctToRemove in DFOfAcctsToRemove: # loop through each acct that we are removing.
                #print(AcctToRemove)
                if AcctToRemove in x:
                    print('Found Account: ', AcctToRemove, '\n')
                    FoundAccts += 1
                    # TODO: you could speed this up by removing the found account from this dataframe. Therefore the next search will be one less.


            # getting index of substrings
            idx1 = x.index('{')
            idx2 = x.index('}')
 
            acct = ''
            # getting elements in between
            for idx in range(idx1+1, idx2):
                acct = acct + x[idx]

            y = x.replace("\"$obj\" acct dive","") 
            f2.write('row: ' + str(rowctr) + ':' + acct + '\n')

        rowctr += 1        

    if FoundAccts != atr:
        print('list of accounts to remove, does not match accounts found in the model. \n')
        input('Please check AccountsReplacement.csv table of accounts to remove. Click enter to exit: ')
        exit()
    else:
        print('all accounts that are going to be removed, were confirmed as found in the model file')

def readWRChangeFile(WRChangelog_fn):
    # Read water rights change file to a data frame
    current_directory = os.getcwd()
    subdirectory_name = "SupportingFiles"
    ReplacementAccounts_filepath = os.path.join(current_directory, subdirectory_name, WRChangelog_fn)

    data = read_csv(ReplacementAccounts_filepath)
    ata = len(data['AccountsToAdd'])
    atr = len(data['AccountsToRemove'])

    # Exit the program if the accounts to add list is a different dimension from the accounts to remove.
    if ata != atr:
        input('list of new accounts does not equal list of old accounts. Please check the account mapping and restart.\n Click enter to exit: ')
    else:
        print('successfully read all new accounts')

    if isna(data).any().any():
        print('NaN\'s (or blanks), encountered in the import file. Please double check the file and try again\n')
        input('Click enter to exit: ')
        exit

    return data

def readfile(filename):
    
    WRData = readWRChangeFile('AccountsReplacement.csv')
    ata = len(WRData['AccountsToAdd'])
    atr = len(WRData['AccountsToRemove'])

    cwd = os.getcwd()
    filename = cwd + '\\' + filename

    f = open(filename, "r")
    f2 = open('ListOfRWAccounts.txt', "w")

    # check all acounts we plan to remove actually exist in the model file:
    CheckEveryAccountToRemoveExists(f,f2,WRData)

    # Loop through each line in the mdl file.
    f.close(), f2.close() #, f3.close(), f4.close()

# Can run main_process.py directly for testing
if __name__ == "__main__":
    cwd = os.getcwd()
    filename = 'DuchesneBasinModel_LFYR_and_URWR_AccountsAdded.mdl'
    readfile(filename)
