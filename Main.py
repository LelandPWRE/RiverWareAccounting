#Import packages here:
import os
import re
import csv
from pandas import *
import shutil

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

# Replace the old accounts with new accounts
def ReplaceAccounts(f,WRData):
    # this function isn't working yet. we need to read and write simultaneously: https://stackoverflow.com/questions/125703/how-to-modify-a-text-file
    lst = ['$obj acct dive ','set o "$obj^','$mgr supply','set o "$mgr.']
    atr_lst = WRData['AccountsToRemove'].tolist()
    ata_lst = WRData['AccountsToAdd'].tolist()
    for x in f: #loop through the entire file
        #print(x)
        for substring in lst:
            if substring in x:
                for AcctToRemove in atr_lst:
                    if AcctToRemove in x:
                        idx = atr_lst.index(AcctToRemove)
                        replacement = ata_lst[idx]
                        x = x.replace(str(AcctToRemove), replacement)
                        #FIXME even after finding and completing the replacement, if the list of replacements hasn't
                        # been completely searched, the algorithm continues.
                        # ??? is it possible to exit the most inner for loop, if the final "if" statement executes?

def CheckEveryAccountToRemoveExists(fr,f2,WRData):
    # This functions searches for every account listed in the AccountsToRemove dataframe in the model text file
    # if the account is found, a counter is updated. The end result of the count of accounts found must be the
    # same length as the accounts planned to remove. If these lengths don't match, the mapping wont work, so we 
    # exit the python script
    DFOfAcctsToRemove = WRData['AccountsToRemove']
    ata = len(WRData['AccountsToAdd'])
    atr = len(WRData['AccountsToRemove'])
    rowctr = 0
    FoundAccts = 0
    for x in fr: # loop through each line in the file

        # check if   "$obj acct dive"   is contained in the string. this restricts our search to account declarations
        if "\"$obj\" acct dive" in x:
            print('row: ', rowctr, '\n')

            for AcctToRemove in DFOfAcctsToRemove: # loop through the list of accts that we are removing.
                #print(AcctToRemove)
                if AcctToRemove in x:
                    print('Found Account: ', AcctToRemove, '\n')
                    FoundAccts += 1
                    # TODO: you could speed this up by removing the found account from this dataframe. 
                    # Therefore the next search will be one less. Marginal gains at best though.


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
        print('successfully read all new accounts from the change file')

    if isna(data).any().any():
        print('NaN\'s (or blanks), encountered in the import file. Please double check the file and try again\n')
        input('Click enter to exit: ')
        exit

    return data

def makebackupfile(filename):
    # this function checks for a preexisting backup file, deletes it if it exists, then creates a new backup file
    # it returns the file path of the backup file.

    cwd = os.getcwd()
    filenameparts = filename.split(".")
    read_dest_filename = filenameparts[0] + "_wNewAccountsRead" + "." + filenameparts[1]
    write_dest_filename = filenameparts[0] + "_wNewAccountsWrite" + "." + filenameparts[1]    
    # src contains the path of the source file 
    src = filename
    # dest contains the path of the destination file 
    destr = read_dest_filename # read
    destw = write_dest_filename # write
    # create duplicate of the file at the destination, 
    try:
        print('checking for pre-existing model file with automatically added accounts')
        os.remove(destr)
        os.remove(destw)
    except Exception as e:
        print('File did not exist. \n')
        print(e)

    path = shutil.copy(src,destr)
    path = shutil.copy(src,destw)
    return [destr, destw]

def readfile(filename):
    
    try:
        WRData = readWRChangeFile('AccountsReplacement.csv')
        print('Succesfully read WRChange file')
    except Exception as e:
        print(e)
        input('failed at readWRChangeFile fxn, click enter to exit')

    ata = len(WRData['AccountsToAdd'])
    atr = len(WRData['AccountsToRemove'])
    cwd = os.getcwd()
    filename = cwd + '\\' + filename

    # remove preexisting auto-file, and create a backup to work in.
    try:
        [destr, destw] = makebackupfile(filename)
    except Exception as e:
        print(e)
        input('failed at makebackupfile function, click enter to exit')

    fr = open(destr, "r") # reading the backup file
    f2 = open('ListOfRWAccounts.txt', "w")

    # check all acounts we plan to remove actually exist in the model file:
    try:
        CheckEveryAccountToRemoveExists(fr,f2,WRData)
        fr.close()
    except Exception as e: 
        print('Exception error encountered when trying to execute CheckEveryAccountToRemoveExists. \n')
        print('Exception error: \n')
        print(e)

    # Replace the old accounts with new accounts
    # ftest = f

    try:
        f = open(destw, "r") # reading the backup file
        ReplaceAccounts(f,WRData)
    except Exception as e: 
        print('Exception error encountered when trying to execute CheckEveryAccountToRemoveExists. \n')
        print('Exception error: \n')
        print(e)

    # Loop through each line in the mdl file.
    f.close(), f2.close() #, f3.close(), f4.close()

# Can run main_process.py directly for testing
if __name__ == "__main__":
    cwd = os.getcwd()
    filename = 'DuchesneBasinModel_LFYR_and_URWR_AccountsAdded.mdl'
    try:
        readfile(filename)
        print('succesfully executed main function')
    except Exception as e:
        print(e)
        print('failed main function')
