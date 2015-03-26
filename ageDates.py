#-------------------------------------------------------------------------------
# Name:        ageDates
# Purpose:     Categorizing levels of severity and age for entries in security
#              vulernibility
# Author:      apatel
#
# Created:     27/02/2015
# Copyright:   (c) apatel 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import comparingCSVsRevised
import csv
import time

""" Run comparingCSVsRevised.py before ageDates.py to receive data """

def ageDates():
    """ Age Date Counting & Severity (Critical, High, Medium, Low) """
    # each entry will have a date and level of severity
    entries = []
    mm_yy = raw_input("Enter Requested Month and Year (ie: 1/15):")
    mm_yy2 = mm_yy.replace("/","_")
    reader = csv.reader(open(mm_yy2 + '_results.csv', 'rb'), delimiter=',')
    for row in reader:
        entries.append([row[8].strip(), row[2].strip()])

    # if null entry, insert to more than 3 months
    emptyStrings = []
    for entry in entries:
        if entry == '':
            emptyStrings.append(1)

    entries = [entry for entry in entries if entry != '']

    # sorting lists
    zeroToOneL = []
    zeroToOneM = []
    zeroToOneH = []
    zeroToOneC = []

    oneToTwoL = []
    oneToTwoM = []
    oneToTwoH = []
    oneToTwoC = []

    twoToThreeL = []
    twoToThreeM = []
    twoToThreeH = []
    twoToThreeC = []

    emptyStringsL = []
    emptyStringsM = []
    emptyStringsH = []
    emptyStringsC = []

    counts =[]

    #todayMonthYear = time.strftime("%m/%y")
    todayMonthYear = mm_yy
    for entry in entries:
        i = comparingCSVsRevised.monthsBetween(mm_yy, entry[0])
        counts.append([i, entry[1]])

    for entry in counts:
        # 0 - 1 months
        if (entry[0] >= 0) and (entry[0] < 1):
            if entry[1] == 'Low':
                zeroToOneL.append(1)
            elif entry[1] == 'Medium':
                zeroToOneM.append(1)
            elif entry[1] == 'High':
                zeroToOneH.append(1)
            elif entry[1] == 'Critical':
                zeroToOneC.append(1)
        # 1 -2 months
        elif (entry[0] >= 1) and (entry[0] < 2):
            if entry[1] == 'Low':
                oneToTwoL.append(1)
            elif entry[1] == 'Medium':
                oneToTwoM.append(1)
            elif entry[1] == 'High':
                oneToTwoH.append(1)
            elif entry[1] == 'Critical':
                oneToTwoC.append(1)
        # 2 - 3 months
        elif (entry[0] >= 2) and (entry[0] < 3):
            if entry[1] == 'Low':
                twoToThreeL.append(1)
            elif entry[1] == 'Medium':
                twoToThreeM.append(1)
            elif entry[1] == 'High':
                twoToThreeH.append(1)
            elif entry[1] == 'Critical':
                twoToThreeC.append(1)
        # > 3 months
        else:
            if entry[1] == 'Low':
                emptyStringsL.append(1)
            elif entry[1] == 'Medium':
                emptyStringsM.append(1)
            elif entry[1] == 'High':
                emptyStringsH.append(1)
            elif entry[1] == 'Critical':
                emptyStringsC.append(1)



    # 0 to 1 months
    sum0to1L = sum(zeroToOneL)
    sum0to1M = sum(zeroToOneM)
    sum0to1H = sum(zeroToOneH)
    sum0to1C = sum(zeroToOneC)
    # 1 to 2 months
    sum1to2L = sum(oneToTwoL)
    sum1to2M = sum(oneToTwoM)
    sum1to2H = sum(oneToTwoH)
    sum1to2C = sum(oneToTwoC)
    # 2 to 3 months
    sum2to3L = sum(twoToThreeL)
    sum2to3M = sum(twoToThreeM)
    sum2to3H = sum(twoToThreeH)
    sum2to3C = sum(twoToThreeC)
    # more than 3 months
    sumElseL = sum(emptyStringsL)
    sumElseM = sum(emptyStringsM)
    sumElseH = sum(emptyStringsH)
    sumElseC = sum(emptyStringsC)

    sum0to1 = ['0 to 1 months:', sum0to1L, sum0to1M, sum0to1H, sum0to1C]
    sum1to2 = ['1 to 2 months:', sum1to2L, sum1to2M, sum1to2H, sum1to2C]
    sum2to3 = ['2 to 3 months:', sum2to3L, sum2to3M, sum2to3H, sum2to3C]
    sumElse = ['> 3 months:', sumElseL, sumElseM, sumElseH, sumElseC]
    header = ['Category', 'Low', 'Medium', 'High', 'Critical']

    # write to csv
    with open(mm_yy2+ '_ageDates.csv', 'wb') as ageDatesCSV:
        writer = csv.writer(ageDatesCSV, delimiter=',')
        writer.writerow(header)
        writer.writerow(sum0to1)
        writer.writerow(sum1to2)
        writer.writerow(sum2to3)
        writer.writerow(sumElse)
    print "(4/5) Complete: Completed writing Age Dates CSV"

def main():
    comparingCSVsRevised.main()
    ageDates()
    print "(5/5) Complete: Age Dates Program Complete."

if __name__ == '__main__':
    main()
