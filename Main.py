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


def readfile(filename):

    f = open(filename, "r")
    f2 = open('ListOfRWAccounts.txt', "w")
    # f3 = open('ListOfSetObjects.txt', "w")
    # f4 = open('oneobject.txt',"w")

    rowctr = 0
    for x in f:
        #print(x)
        # check if   "$obj acct dive"   is contained in the string
        if "\"$obj\" acct dive" in x:
            print(rowctr)
            print(x)
           
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

    import os

    current_directory = os.getcwd()
    subdirectory_name = "SupportingFiles"
    file_name = "AccountsReplacement.csv"
    ReplacementAccounts_filepath = os.path.join(current_directory, subdirectory_name, file_name)
    

    # open/read the new accounts mapping file.
    # accts_listofdictionaries = []
    # with open(ReplacementAccounts_filepath, 'r') as file:
    #     dict_reader = csv.DictReader(file)
    #     for line in dict_reader:
    #         accts_listofdictionaries.append(line)

    # accts_dict = {}
    # for d in accts_listofdictionaries:
    #     accts_dict.update(d)

    # print(accts_dict)

    data = read_csv(ReplacementAccounts_filepath)
    AcctsToAdd = data['AccountsToAdd'].tolist
    AcctsToRemove = data['AccountsToRemove'].tolist
    ata = len(AcctsToAdd)
    atr = len(AcctsToRemove)

    if ata != atr:
        input('list of new accounts does not equal list of old accounts. Please check the account mapping and restart.\n Click enter to exit: ')


            
    f.close(), f2.close() #, f3.close(), f4.close()

# Can run main_process.py directly for testing
if __name__ == "__main__":
    cwd = os.getcwd()
    filename = cwd + '\\DuchesneBasinModel_LFYR_and_URWR_AccountsAdded.mdl'
    readfile(filename)
