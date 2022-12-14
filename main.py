#!/usr/bin/python

"""
=============================================================================
Filename      : abbrevator
Author        : Sunderam Palavesam
Date Created  : 22 Nov 2022
=============================================================================
Description   : Abbrevation generator for any string based on Rules
                Developed as part of course work AC
                Developed as part of Python assignment Msc course Work
                Dundee University
Revisions
=============================================================================
221122   2474761 AC50002  initial version                               1.0
=============================================================================
"""

# import the required libraries
import sys
import itertools
import re
import os
import argparse

"""
function to parse inputs and provide usage
"""
def getOptions(argv):
  global inputFile
  global outputFile

  inputFile = ''
  arg_parser = argparse.ArgumentParser( description = "Abbrevate the words in given file" )
  arg_parser.add_argument( "input_file" )
  arguments = arg_parser.parse_args()

  inputFile = arguments.input_file
  print( "Input File is [{}] ".format(inputFile) )


"""
function to read input file
calls computeCombinations for each input string
"""
def readInputFile():
  # dict of dict nested structure which stores the input string
  # and all abbrevations along with scores
  global data
  # dict of dict nested structure which stores the final output
  # string with abbrevation having minimum score
  global dataOut
  # list having unique abbrevations
  # used as lookup to ensure unique values are only maintained
  global uniqueList
  # list having duplicate abbrevations
  # used as lookup to avoid duplicates
  global dupeList

  data = {}
  dataOut={}
  uniqueList = []
  dupeList = []
 
  with open(inputFile) as f:
    for line in f:
      inString=(line.strip().upper())
      # for each input string , get all 3 letter abbrevations
      computeCombinations(inString)

 
  for i in data:
    for k in dupeList:
      if k in data[i].keys():
        #remove dupes
        del data[i][k]

    #compute scores after removing the dupes
    for e in data[i].keys():
      if data[i][e] != 0:
        score = computeScore(i,e)
        data[i][e] = score


"""
function to write output file
loops through outputdata and writes the
abbrevations with minimum score
"""
def writeOutputFile():
  inFile=os.path.basename(inputFile).split('.')[0]
  outputFile="Palavesam_" + inFile + "_abbrevs.txt"
  print('Output file is ', outputFile)

  for i in data:
    mintemp={}
    minscore=0
    c=0

    for k in data[i].keys():
      tempscore=data[i][k]
      c=c+1
      if tempscore<minscore or c == 1:
        minscore=tempscore
        abbr=k
   
    if c>0:
      #set the abbrevation with minimum score
      mintemp[abbr]=minscore
      dataOut[i] = mintemp
 
  print(data)
  print(dataOut)
  print(dupeList)
  
  # write to output file
  with open(outputFile, 'w') as f:
    for i in data:
      f.write(i + '\n')
      if i in dataOut:
        for k in dataOut[i].keys():
          f.write(k + '\n')
      else:
        f.write('\n')

"""
function to find all 3 letter abbrevations
 - uses itertools combinations
 - ensures abbrevations starts with first char of the
    string to keep score to minimum
- logic to handle multiple words split by space
- ensures that first chars are used for strings
  with multipe words
"""
def computeCombinations(str):

  #clean the string
  str = re.sub('[^A-Za-z ]+', '', str)

  # hold temp results
  restemp = {}
  strtemp = ''
  strspacetemp = ''

  # if multiple words , split by space and select first chars to get 0 score.
  # handles cases like Object Oriented Prog
  for s in str.split():
    strspacetemp = strspacetemp + (''.join(s[0]).upper())
    if len(strspacetemp) >= 3:
      strspacetemp = strspacetemp[0:3]
      restemp[strspacetemp] = 0
      uniqueList.append(strspacetemp)


  # get all 3 char combinations without space this time.
  str = re.sub('[^A-Za-z]+', '', str)
  strtemp = ''
  firstchar=str[:1]
  # magic happens here
  t=itertools.combinations(str,3)
  for i in t:
    strtemp = (''.join(i).upper())
    if strtemp.startswith(firstchar) and len(strtemp) == 3 and strtemp != strspacetemp:
      if strtemp not in dupeList:
        if strtemp not in uniqueList:
          restemp[strtemp] = -1
          uniqueList.append(strtemp)
          data[str] = restemp
        elif strtemp in uniqueList:
          uniqueList.remove(strtemp)
          dupeList.append(strtemp)  
   
"""
function to compute the score for given input string
"""

def computeScore(inString,instringAbbr):
  secondchar=inString[1]
  thirdchar=inString[2]
  lastchar=inString[len(inString)-1]
  score=0

  for c in instringAbbr[1:]:
    tempscore = 0
    match c:
      case c if c == lastchar:
        if c != "E":
          tempscore = 5
        elif c == "E":
          tempscore = 20
      case c if c == secondchar:
        tempscore = 1 + computeScoreByRules(c)
      case c if c == thirdchar:
        tempscore = 2 + computeScoreByRules(c)
      case _:
        tempscore = 3 + computeScoreByRules(c)
    score += tempscore

  return score

"""
Helper function to assist in score calculation
scores are based on position and alphabet.
"""

def computeScoreByRules(c):
  match c:
    case c if c in ("Q", "Z"):
      return 1
    case c if c in ("J", "X"):
      return 3
    case c if c in ("K"):
      return 6
    case c if c in ("F","H","V","W","Y"):
      return 7
    case c if c in ("B","C","M","P"):
      return 8
    case c if c in ("D","G"):
      return 9
    case c if c in ("L","N","R","S","T"):
      return 15
    case c if c in ("O","U"):
      return 20
    case c if c in ("A","I"):
      return 25
    case c if c in ("E"):
      return 35
    case _:
      return 0

"""
Main function
"""

def main(argv):
  getOptions(argv)
  readInputFile()
  writeOutputFile()
 

if __name__ == "__main__":
   main(sys.argv[1:])
