'''Artificial Intelligence Homework 2
Yusuf Ekiz 150120040'''

from simpleai.search import CspProblem,convert_to_binary
from simpleai.search import backtrack, MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE
import re #Regular expression library


class PickPix(object):
    def __init__(self):

        self.numberOfColumns = None  # equals to row size
        self.numberOfRows = None # equals to column size

        self.rowClues = [] # initially rowclues and column clues are empty
        self.columnClues = []

        self.readCluesFromFile()

        self.cellVariablesTuple = None
        self.cellDomains = None
        self.cellConstraints = None

        self.cellVariables = self.initializeCellVariables() #Initialize cell variables
        self.cellVariablesTuple = tuple(self.cellVariables)
        #convert variables list to tuple. SimpleAI expects tuple instead of list '''

        self.initializeCellVariableDomains() #Initialize domains
        self.initializeDimensionConstraints() #Initialize constraints

        print 'Variables =', self.cellVariablesTuple  #Print variables
        print #empty line
        '''print 'Domains = ', self.cellDomains #Print domains
        print
        print 'Constraints =', self.cellConstraints #Print constraints
        print'''
        self.solution = None #At first solution will be None

    def solve(self):

        print 'Please wait while AI is solving the puzzle'
        print
        print

        self.cellVariablesTuple, self.cellDomains, self.cellConstraints = convert_to_binary(self.cellVariablesTuple, self.cellDomains,
                                                                                self.cellConstraints) #convert fields to binary

        problem = CspProblem(self.cellVariablesTuple,self.cellDomains,self.cellConstraints) # initialize the csp problem
        self.solution = backtrack(problem) #solve the csp problem.
        print 'CSP Problem Is Solved'
        print
        self.printSolution() #print the solution

        return

    def readCluesFromFile(self):

        input_file = open('example_input.txt', 'r')
        self.numberOfRows = int(input_file.readline())

        for rowIndex in range(0,self.numberOfRows): #read row clues
            line = input_file.readline().strip()
            currentRowClue = [int(i) for i in line.split(" ")]
            self.rowClues.append(currentRowClue)
        self.numberOfColumns = int(input_file.readline())

        for columnIndex in range(0,self.numberOfColumns): #read column clues
            line = input_file.readline().strip()
            currentColumnClue = [int(j) for j in line.split(" ")]
            self.columnClues.append(currentColumnClue)

    def initializeCellVariables(self):

        variableString = ''
        for rowIndex in range(0,self.numberOfRows):
            for columnIndex in range(0,self.numberOfColumns):
                variableString = variableString + 'Cell Row:' +str(rowIndex)+' Column:'+ str(columnIndex)
                if columnIndex != self.numberOfColumns - 1 or rowIndex != self.numberOfRows -1:#If it is not last element put comma for the next element.
                    variableString = variableString + ','

        return variableString.split(',')

    def initializeCellVariableDomains(self):

        allVariables = self.cellVariables #get variable list
        domainDictionary = {} #create an empty dictionary
        for index in range(0,len(allVariables)):
            variableName = allVariables[index] #get the current variable
            elementDomain = [' ','#']  #create domain for element
            domainDictionary[variableName] = elementDomain #map the variable to the domain
        self.cellDomains = domainDictionary #initialize cell Domains

    def initializeDimensionConstraints(self):
        constraintList = [] # initialize empty list.

        for currentRowIndex in range(0,self.numberOfRows): #initialize dimensionClueConstraint every row
            currentRow = [] # at first currentRow is empty

            for index in range(0,len(self.cellVariables)): # search all variables with currentRow index
                number = self.parseRowIndexFromCell(self.cellVariables[index])
                if number == currentRowIndex: #if number equals the current row index add cell to the current row list
                    currentRow.append(self.cellVariables[index])
            rowTuple = tuple(currentRow) #convert row to the tuple
            constraintList.append((rowTuple,self.dimensionClueConstraint)) # add row with its constraint

        for currentColumnIndex in range(0,self.numberOfColumns):
            currentColumn = []
            for index in range(0,len(self.cellVariables)): #search all variables with currentColumnIndex
                number = self.parseColumnIndexFromCell(self.cellVariables[index])
                if number == currentColumnIndex:
                    currentColumn.append(self.cellVariables[index]) #if number equals current column index add cell to the current column list
            columnTuple = tuple(currentColumn)
            constraintList.append((columnTuple,self.dimensionClueConstraint)) #add column with its constraint

            self.cellConstraints = constraintList #initialize cellConstraints field

        return

    def dimensionClueConstraint(self, variables, values):

        isRow = False
        if self.parseRowIndexFromCell(variables[0]) == self.parseRowIndexFromCell(variables[1]): # check is itRow or not.
            isRow = True

        if isRow == True: #if Row initialize fields with row functions.
            dimensionIndex = self.parseRowIndexFromCell(variables[0])
            clue = self.rowClues[dimensionIndex]
            size = self.numberOfColumns # row size = number of columns
        else:#else initialize fields with column functions
            dimensionIndex = self.parseColumnIndexFromCell(variables[0])
            clue = self.columnClues[dimensionIndex]
            size = self.numberOfRows # column size = number of rows

        numberOfBlocks = len(clue) # get the number of blocks frum clue
        blackCellNumber = 0 # find number of block cells from clue
        for num in range(0, len(clue)):
            blackCellNumber = blackCellNumber + clue[num]

        realBlackCells = 0 #find real number of block cells from the variable which is a row or a column.
        for num in range(0, len(values)):
            if values[num] == '#':
                realBlackCells += 1

        if realBlackCells != blackCellNumber: #Black cell numbers are not equal, so it does not fit the structure.Return false.
            return False

        blockIndex = 0  #start from block with index 0
        isLastBlock = False #initialize is Last block false
        index = 0 #start row element index from 0.

        while index < size: # while loop for iterating the row or column
            lengthOfCurrentBlock = clue[blockIndex] # get the length of current block.
            cellValue = values[index] # get the cell value from row or column
            if cellValue == '#': #If the cell value is black check it is last block or not.
                if blockIndex == numberOfBlocks - 1:
                    isLastBlock = True

                for j in range(0, lengthOfCurrentBlock - 1): #for loop for iterate over current block.
                    index += 1
                    if (index >= size): #if index is bigger than row size, return false.
                        return False
                    cellValue = values[index]
                    if cellValue == ' ': #if we have empty cell in current block return false too.
                        return False
                if isLastBlock == False and index < size - 1: # If it is not last block and there are still cells left
                    index += 1 # go to the next cell
                    cellValue = values[index]
                    if cellValue == '#': #if we don't have an empty cell, it doesn't fit constraint too. return false.
                        return False
                blockIndex += 1 #increment block index

            if isLastBlock == True: #if it is last block
                if index < size - 1: #check the rest of cells are white or not.
                    for k in range(index + 1, size):
                        cellValue = values[k]
                        if cellValue == '#':
                            return False #If not return false
                    return True #else return true
                else:
                    return True #return true
            index = index + 1
        return True #return true.Loop is finised.

    def parseRowIndexFromCell(self,variable):
        numbers = [int(s) for s in re.findall(r'\b\d+\b',variable)]
        #Re is a regular expression library which is helpful for parsing strings
        index = int(numbers[0]) #Row index comes before column index. So we will take numbers[0]
        return index

    def parseColumnIndexFromCell(self,variable):
        numbers = [int(s) for s in re.findall(r'\b\d+\b',variable)]
        # Column index comes after row index. So we will take numbers[1]
        index = numbers[1]
        return index

    def printSolution(self):

        for rowIndex in range (0,self.numberOfRows):
            for columnIndex in range(0,self.numberOfColumns):
                valueKey = 'Cell Row:' + str(rowIndex) +' Column:' + str(columnIndex)
                value = self.solution[valueKey]
                print value,
            print
        return

if __name__ == '__main__':
    PickPix().solve() #Create an object of PickPix class then call the solve function.
