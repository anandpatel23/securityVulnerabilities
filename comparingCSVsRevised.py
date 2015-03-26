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
import os
import itertools
import time


"""
NOTES (READ BEFORE EXECUTION):
    - Convert xlsx to CSV
    - Delete empty rows
    - find and replace all dates in comments section to just dates
    - If you're entering a date like 08/14, enter 8/14. [Remove excess zeros]
    - convert excel files to CSV before executing.
    - 2 input files:
        - Base [Results]
        - New [Tenible Export]
    - 3 output files:
        - "date"_results -> (base rows) and (new rows that are not in base)
        - "date"_resolved -> base rows that are not in new
        - "ageDate" -> Tracking ages of entries in months
    - format csv where age date column has: mm/yy
    - have all files in the same folder (includes this script)

"""

def newEntriesCols(row):
    """ Columns in Tenible Export -> New """
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

def baseEntriesCols(row):
    """ Columns in Results -> Base"""
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
    from datetime import datetime
    return str()

def monthsBetween(d1, d2):
    from datetime import datetime
    d2 = d2.strip()
    d1 = datetime.strptime(d1, "%m/%y")
    d2 = datetime.strptime(d2, "%m/%y")
    day = abs((d2 - d1).days)
    return day/30

def main():
    # User input files to program
    baseFile = raw_input("Enter Name of Base file (ie: Results.csv):")
    baseFile2 = baseFile
    newFile = raw_input("Enter Name of New File (ie: Tenable.csv):")
    newFile2 = newFile
    mm_yy = raw_input("Enter Requested Month and Year (ie: 1/15):")
    mm_yy2 = mm_yy.replace("/","_")

    """If the Plugin, IP Address, and Port are in new (tenible) and NOT in base (results), insert into base """
    # Open CSV Reading
    with open(newFile, 'rb') as newFile:
        with open(baseFile, 'rb') as baseFile:
            newCSVReader = csv.DictReader(newFile)
            baseCSVReader = csv.DictReader(baseFile)

            # Columns for comparison are Plugin, IP Address, and Port
            newEntries = []
            for row in newCSVReader:
                newEntries.append(newEntriesCols(row))

            # Repeat for second file
            baseEntries = []
            for row in baseCSVReader:
                baseEntries.append(baseEntriesCols(row))
                if row['Owner'] == '':
                    row['Owner'] = 'Null'

            resultsList = []
            # CSV Entries
            oldResults = mm_yy2+'_testresults.csv'
            with open(mm_yy2 +'_testresults.csv','wb') as resultsCSV:
                writer = csv.writer(resultsCSV, delimiter=',')
                # Find and match process
                for n in newEntries:
                    match = False
                    for b in baseEntries:
                        if ((b[0] == n[0]) and (b[3] == n[3]) and (b[4] == n[4])):
                            match = True
                            break
                    if(not match):
                        n[8] = mm_yy
                        writer.writerows([n])
                        resultsList.append(n)
                for b in baseEntries:
                    writer.writerows([b])
                    resultsList.append(b)
                print "(1/5) Complete: New entries have been added to the base file"

    """ If the Plugin, IP Address, and Port are in base (results) and not in new (tenible), insert to new CSV for Resolved """
    # Open CSV Reading
    with open(baseFile2, 'rb') as baseFile2:
        with open(newFile2, 'rb') as newFile2:
            baseCSVReader2 = csv.DictReader(baseFile2)
            newCSVReader2 = csv.DictReader(newFile2)

            # Columns for comparison are Plugin, IP Address, and Port
            baseEntries2 = []
            for row in baseCSVReader2:
                baseEntries2.append(baseEntriesCols(row))

            newEntries2 = []
            # Repeat for second file
            for row in newCSVReader2:
                newEntries2.append(newEntriesCols(row))

            resolvedList = []
            # CSV Entries
            with open(mm_yy2 +'_resolved.csv', 'wb') as resolvedCSV:
                writer = csv.writer(resolvedCSV, delimiter=',')

                # Find and match process
                for b in baseEntries2:
                    found = False
                    for n in newEntries2:
                        if ((b[0] == n[0]) and (b[3] == n[3]) and (b[4] == n[4])):
                            found = True
                            break
                    if(not found):
                            writer.writerows([b])
                            resolvedList.append(b)
                print "(2/5) Complete: Base files that were not found in New have been copied to Resolved"

    """ Remove base entries if they are in resolved """
    finalResultsList = []

    for result in resultsList:
        for resolved in resolvedList:
            if result == resolved:
                break
        else:
            finalResultsList.append(result)

    with open(mm_yy2+'_results.csv', 'wb') as resultsFinalCSV:
        writer = csv.writer(resultsFinalCSV, delimiter=',')
        for result in finalResultsList:
            writer.writerows([result])
    print "(3/5) Complete: Added results without base entries that are in resolved now"

    os.remove(oldResults)
if __name__ == '__main__':
    main()
