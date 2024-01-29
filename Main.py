#Import packages here:
import os
import re

"""
Overview
Purpose: Automate adding accounts to RiverWare
Python: version 3.8.1
Author: Leland Dorchester
"""

def readfile(filename):

    f = open(filename, "r")
    f2 = open('ListOfRWAccounts.txt', "w")
    f3 = open('ListOfSetObjects.txt', "w")
    f4 = open('oneobject.txt',"w")
    #trigger = False
    for x in f:
        #print(x)
        # check if   "$obj acct dive"   is contained in the string
        #if "\"$obj\" acct dive" in x:
        #    f2.write(x)
        # create a list of set objects in the model for txt file syntax analysis
        if "set obj" in x:
            f3.write(x)

        # if trigger:
        #     print(x)

        if "set obj \"$ws." in x:
            #trigger = True
            x = next(f, None)   # update to the next line in the file
            while "set obj \"$ws." not in x:
                f4.write(x)     # write the contents of the object to a temp holding file for troubleshooting
                
                if x is None:
                    break       # Exit the loop if there are no more lines in the file
                
                # write the account name to the list of RW accounts file (ListOfRWAccounts.txt)
                if "\"$obj\" acct dive " in x:
                    startidx = x.find("{")
                    endidx = x.find("}")
                    acctname = x[startidx+1:endidx]
                    f2.write("\n" + acctname)
                    x = x.replace(acctname,"TestAccount")

                x = next(f, None)


            f4.write('\n\n ********** NEXT OBJECT ********** \n\n')
            


    f.close(), f2.close(), f3.close(), f4.close()

# Can run main_process.py directly for testing
if __name__ == "__main__":
    cwd = os.getcwd()
    filename = cwd + '\\DuchesneBasinModel_LFYR_and_URWR_AccountsAdded.mdl'
    readfile(filename)
