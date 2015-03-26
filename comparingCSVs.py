#-------------------------------------------------------------------------------
# Name:        comparingCSVs
# Purpose:     Compare CSVs for New, Resolved, or both
#
# Author:      apatel
#
# Created:     23/01/2015
# Copyright:   (c) apatel 2015
# Licence:     None
#-------------------------------------------------------------------------------
import csv
import datetime

"""
NOTES (READ BEFORE EXECUTION):
    - Delete empty rows
    - If you're entering a date like 08/14, enter 8/14. [Remove excess zeros]
    - convert excel files to CSV before executing.
    - 2 input files:
        - Base [Results]
        - New [Tenible Extract]
    - 2 output files:
        - "date"_results -> (base rows) and (new rows that are not in base)
        - "date"_resolved -> base rows that are not in new
    - format csv where age date column has: mm/yy
    - have all files in the same folder (includes this script)

"""

def newEntriesCols(row):
    return [
            row['Plugin'],
            row['Plugin Name'],
            row['Severity'],
            row['IP Address'],
            row['Port'],
            row['Protocol'],
            row['Family'],
            row['DNS Name'],
            row['NetBIOS Name'],
            row['First Discovered'],
            row['Last Observed']
            ]

def baseEntriesCols(row):
    return [
            row['Plugin'],
            row['Plugin Name'],
            row['Severity'],
            row['IP Address'],
            row['Port'],
            row['Protocol'],
            row['Family'],
            row['Owner'],
            row['Age Date'],
            row['DNS Name'],
            row['NetBIOS Name'],
            row['First Discovered'],
            row['Last Observed']
            ]

def dateAsString():
    return datetime.datetime.today().strftime('%Y%m%d')

def insertNewInBase(newCSV, baseCSV, monthyear):
    """If the Plugin, IP Address, and Port are in new (tenible) and NOT in base (results), insert into base """
    # Open CSV Reading
    with open(newCSV, 'rb') as newCSV:
        with open(baseCSV, 'rb') as baseCSV:
            newCSVReader = csv.DictReader(newCSV)
            baseCSVReader = csv.DictReader(baseCSV)

            # Columns for comparison are Plugin, IP Address, and Port
            newEntries = []
            for row in newCSVReader:
                newEntries.append(newEntriesCols(row))

            # Repeat for second file
            baseEntries = []
            for row in baseCSVReader:
                baseEntries.append(baseEntriesCols(row))

            # CSV Entries
            with open(dateAsString()+'_results.csv','wb') as resultsCSV:
                writer = csv.writer(resultsCSV, delimiter=',')
                # Find and match process
                for n in newEntries:
                    match = False
                    for b in baseEntries:
                        if ((b[0] == n[0]) and (b[3] == n[3]) and (b[4] == n[4])):

                            match = True
                            break
                    if(not match):
                        n[8] = monthyear
                        writer.writerows([n])
                for b in baseEntries:
                    writer.writerows([b])
                print "insertNewInBase() completed"


def insertBaseInNew(baseCSV, newCSV, monthyear):
    """ If the Plugin, IP Address, and Port are in base (results) and not in new (tenible), insert to new CSV for Resolved """
    # Open CSV Reading
    with open(baseCSV, 'rb') as baseCSV:
        with open(newCSV, 'rb') as newCSV:
            baseCSVReader = csv.DictReader(baseCSV)
            newCSVReader = csv.DictReader(newCSV)

            # Columns for comparison are Plugin, IP Address, and Port
            baseEntries = []
            for row in baseCSVReader:
                baseEntries.append(baseEntriesCols(row))

            newEntries = []
            # Repeat for second file
            for row in newCSVReader:
                newEntries.append(newEntriesCols(row))

            # CSV Entries
            with open(dateAsString() +'_resolved.csv', 'wb') as resolvedCSV:
                writer = csv.writer(resolvedCSV, delimiter=',')

                # Find and match process
                for b in baseEntries:
                    found = False
                    for n in newEntries:
                        if ((b[0] == n[0]) and (b[3] == n[3]) and (b[4] == n[4])):
                            found = True
                            break
                    if((not found) and (monthyear in b[8])):
                            writer.writerows([b])
                print "insertBaseInNew() completed"

def main():
    # User input files to program
    baseFile = raw_input("Enter name of Base file (ie: baseTest.csv):")
    newFile = raw_input("Enter name of New File (ie: newTest.csv):")
    mm_yy = raw_input("Enter date (ie: 1/15):")

    # run modules
    try:
        insertNewInBase(newFile, baseFile, mm_yy)
    except:
        "Error has occured within insertNewInBase()"

    try:
        insertBaseInNew(baseFile, newFile, mm_yy)
    except:
        "Error has occured within insertBaseInNew()"

if __name__ == '__main__':
    main()
