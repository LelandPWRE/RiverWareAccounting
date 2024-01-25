#Import packages here:
import os

"""
Overview
Purpose: Automate adding accounts to RiverWare
Python: version 3.8.1
Author: Leland Dorchester
"""

def readfile(filename):
    print('2: ', filename)


# Can run main_process.py directly for testing
if __name__ == "__main__":
    cwd = os.getcwd()
    filename = cwd + 'DuchesneBasinModel_LFYR_and_URWR_AccountsAdded.mdl'
    readfile(filename)
