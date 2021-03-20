# CS 6320 - Natural Language Processing - Spring 2020
# Written by Kamin Bouguyon
# Homework 1: Regular Expressions
# Goal: Extract time and date information from a given corpus.

import re
import sys

dateStrings = []
inputFile = ''
outputFile = 'dates.txt'

# regular expressions
dayReg = r'\b[0123]?\d(st|nd|th)?\b'
monthNumReg = r'\b[01]?\d\b'
monthReg = r'\b([jJ]an(uary)?|[fF]eb(ruary)?|[mM]ar(ch)?|[aA]pr(il)?|[mM]ay|[jJ]une?|[jJ]uly?|[aA]ug(ust)?|[sS]ept?(ember)?|[oO]ct(ober)?|[nN]ov(ember)?|[dD]ec(ember)?)\b'
yearReg = r'\b[12]\d{2,3}( [bB]?[cC][eE])?\b'

def year(string):
    return re.search(yearReg, string)

def yearRange(string):
    return re.search('{y} ?[-–] ?{y}'.format(y=yearReg), string)

def date(string):
    return re.search('({m}( {d})?(,? {y})?|{M}[/-–]{d}[/-–]{y})'.format(m=monthReg, M=monthNumReg, d=dayReg, y=yearReg), string)

# TODO: make this prettier
# Final act, output found dates as strings
def printDates():
    o = open(outputFile, 'w')
    for date in dateStrings:
        o.write (date + '\n')
    o.close()

# recursive parsing function to retrieve all matches in a line
def parse(line):
    # start with matching a year range
    match = yearRange(line)
    if match and match.start() != -1:
        dateStrings.append(match.group())
        parse(line[:match.start()] + line[match.end():])
        return

    # next match dates
    match = date(line)
    if match and match.start() != -1:
        dateStrings.append(match.group())
        parse(line[:match.start()] + line[match.end():])
        return

    # finally catch any isolated years remaining
    match = year(line)
    if match and match.start() != -1:
        dateStrings.append(match.group())
        parse(line[:match.start()] + line[match.end():])
        return

# Entry point, pulls corpus file name from command line
def main():
    if len(sys.argv) < 2:
        raise ValueError('Please include the file name of your corpus.')
    if len(sys.argv) == 3:
        global outputFile
        outputFile = sys.argv[2]
    inputFile = sys.argv[1]
    f = open(inputFile, "r")
    for line in f:
        parse(line)
    f.close()

main()
printDates()
