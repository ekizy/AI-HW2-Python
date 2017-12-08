from simpleai.search import CspProblem,convert_to_binary
from simpleai.search import backtrack,MOST_CONSTRAINED_VARIABLE,LEAST_CONSTRAINING_VALUE


class PickPix(object):
    def __init__(self):

        self.countColumn = 0
        self.countRow = 0

        self.numberOfColumns = None  # equals to row size
        self.numberOfRows = None # equals to column size

        self.rows = None
        self.columns = None

        self.rowDomains = []
        self.columnDomains = []

        self.rowConstraints = []
        self.columnConstraints = []

        self.variables = None
        self.domains = None
        self.constraints = None

        self.constraints = []
        self.readConstraintsFromFile()

        self.initializeVariables()
        self.variablesTuple = tuple(self.variables)

        self.cellDomains = None
        self.cellConstraints = None

        self.cellVariables = self.initializeCellVariables()
        self.cellVariablesTuple = tuple(self.cellVariables)
        self.initializeCellVariableDomains()
        self.initializeDimensionConstraints()

        print (self.cellVariablesTuple)
        print(self.cellDomains)
        print(self.cellConstraints)

        self.cellVariablesTuple, self.cellDomains, self.cellConstraints = convert_to_binary(self.cellVariablesTuple, self.cellDomains,
                                                                                self.cellConstraints)

        problem = CspProblem(self.cellVariablesTuple,self.cellDomains,self.cellConstraints)

        result = backtrack(problem,variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                   value_heuristic=LEAST_CONSTRAINING_VALUE)

        print (result)


        '''self.makeRowDomain(0,[])
        self.makeColumnDomain(0,[])

        self.rows = self.getRows()
        self.columns = self.getColumns()

        self.rowsTuple = tuple(self.rows)
        self.columnsTuple = tuple(self.columns)

        self.initializeDomains()
        self.initializeConstraints()

        #print(self.variablesTuple)
        #print(self.domains)
        #print(self.constraints)'''

        '''self.variablesTuple,self.domains,self.constraints = convert_to_binary(self.variablesTuple,self.domains,self.constraints)

        problem = CspProblem(self.variablesTuple,self.domains,self.constraints)

        result = backtrack(problem,variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                   value_heuristic=LEAST_CONSTRAINING_VALUE)

        print (result)'''



    def solve(self):
        print ('asd')
        return
    def const_row(self,variables,values):
        return
    def readConstraintsFromFile(self):
        input_file = open('example_input.txt', 'r')
        self.numberOfRows = int(input_file.readline())
        for rowIndex in range(0,self.numberOfRows):
            line = input_file.readline().strip()
            currentRowConstraint = [int(i) for i in line.split(" ")]
            self.rowConstraints.append(currentRowConstraint)
        self.numberOfColumns = int(input_file.readline())
        for columnIndex in range(0,self.numberOfColumns):
            line = input_file.readline().strip()
            currentColumnConstraint = [int(j) for j in line.split(" ")]
            self.columnConstraints.append(currentColumnConstraint)

    def initializeVariables(self):
        variablesString = ''
        for rowIndex in range(0,self.numberOfRows):
            variablesString = variablesString + 'Row ' + str(rowIndex + 1) + ','

        for columnIndex in range(0,self.numberOfColumns):
            variablesString = variablesString + 'Column '+ str(columnIndex+1)
            if(columnIndex != self.numberOfColumns - 1):
                variablesString = variablesString + ','

        self.variables = variablesString.split(',')


    def initializeCellVariables(self):
        variableString = ''
        for rowIndex in range(0,self.numberOfRows):
            for columnIndex in range(0,self.numberOfColumns):
                variableString = variableString + 'Cell' +str(rowIndex)+str(columnIndex)
                if columnIndex != self.numberOfColumns - 1 or rowIndex != self.numberOfRows -1:
                    variableString = variableString + ','

        return variableString.split(',')

    def initializeCellVariableDomains(self):

        allVariables = self.cellVariables
        domainDictionary = {}
        for index in range(0,len(allVariables)):
            variableName = allVariables[index]
            elementDomain = [0,1]
            domainDictionary[variableName] = elementDomain
        self.cellDomains = domainDictionary


    def initializeDomains(self):
        allVariables = self.variables
        domainDictionary = {}
        for index in range(0,len(allVariables)):
            variableName = allVariables[index]
            elementDomain = []
            if 'Row' in variableName:
                elementDomain = self.rowDomains
            elif 'Column' in variableName:
                elementDomain = self.columnDomains
            else:
                raise IOError
            domainDictionary[variableName] = elementDomain
        self.domains = domainDictionary


    def makeColumnDomain(self,cellIndex,tempColumnDomain):
        for i in range(0,2): # every cell has 2 possible values
            if cellIndex == self.numberOfRows:
                self.columnDomains.append(tempColumnDomain)
                return
            newList = tempColumnDomain + [i]
            self.makeColumnDomain(cellIndex + 1,newList)

    def makeRowDomain(self,cellIndex,tempRowDomain):
        for i in range(0,2): # every cell has 2 possible values
            if cellIndex == self.numberOfColumns:
                self.rowDomains.append(tempRowDomain)
                return
            newList = tempRowDomain + [i]
            self.makeRowDomain(cellIndex + 1,newList)

    def getRows(self):
        rowsString = ''
        rowCounter = 0
        for variableIndex in range(0,len(self.variables)):
            if 'Row' in self.variables[variableIndex]:
                rowsString = rowsString + self.variables[variableIndex]
                if rowCounter < self.numberOfRows - 1:
                    rowsString = rowsString + ','
                    rowCounter += 1

        return rowsString.split(',')

    def getColumns(self):
        columnsString = ''
        columnCounter = 0
        for variableIndex in range(0,len(self.variables)):
            if 'Column' in self.variables[variableIndex]:
                columnsString = columnsString + self.variables[variableIndex]
                if columnCounter < self.numberOfColumns -1:
                    columnsString = columnsString + ','
                    columnCounter+= 1

        return columnsString.split(',')

    def initializeDimensionConstraints(self):
        constraintList = []

        for rowIndex in range(0,self.numberOfRows):
            row = []
            for index in range(0,len(self.cellVariables)):
                number = self.parseRowIndexFromCell(self.cellVariables[index])
                if number == rowIndex:
                    row.append(self.cellVariables[index])
            rowTuple = tuple(row)
            constraintList.append((rowTuple,self.clueConstraint))

        for columnIndex in range(0,self.numberOfColumns):
            column = []
            for index in range(0,len(self.cellVariables)):
                number = self.parseColumnIndexFromCell(self.cellVariables[index])
                if number == columnIndex:
                    column.append(self.cellVariables[index])
            columnTuple = tuple(column)
            constraintList.append((columnTuple,self.clueConstraint))

            self.cellConstraints = constraintList

        return
    def initializeConstraints(self):
        constraintList = []
        #constraintList.append((self.variablesTuple,self.rowColumnConsistency))
        
        for i in range(0,self.numberOfRows):
            tupleRow = (self.rows[i],)
            constraintList.append((tupleRow,self.rowClueConstraint))

        for j in range(0,self.numberOfColumns):
            tupleColumn = (self.columns[j],)
            constraintList.append((tupleColumn,self.columnClueConstraint))

        self.constraints = constraintList
        return

    def rowColumnConsistency(self,variables,values):

        rowValues = []
        columnValues = []

        for i in range(0, len(variables)):
            if 'Row' in variables[i]:
                rowValues.append(values[i])
            elif 'Column' in variables[i]:
                columnValues.append(values[i])
            else:
                raise IOError

        for rowIndex in range(0,len(rowValues)):
            for columnIndex in range(0,len(columnValues)):
                if(rowValues[rowIndex][columnIndex] != columnValues[columnIndex][rowIndex]):
                    return False
        return True


    def rowClueConstraint(self,variables,values):

        for elementIndex in range(0,len(variables)):

            number = self.parseNumberFromVariable(variables[elementIndex])

            rowSize = self.numberOfColumns

            rowClue = self.rowConstraints[number]

            rowValues = values[elementIndex]

            numberOfBlocks = len(rowClue)

            blackCellNumber = 0

            for num in range(0,len(rowClue)):
                blackCellNumber = blackCellNumber + rowClue[num]

            realBlackCells = 0

            for num in range(0,len(rowValues)):
                if rowValues[num] == 1:
                    realBlackCells +=1

            if realBlackCells != blackCellNumber:
                return False

            blockIndex = 0

            isLastBlock = False

            index = 0

            while index < rowSize:
                lengthOfCurrentBlock = rowClue[blockIndex]
                cellValue = rowValues[index]

                if cellValue == 1:
                    if blockIndex == numberOfBlocks - 1:
                        isLastBlock = True

                    for j in range(0,lengthOfCurrentBlock - 1):
                        index+=1
                        if(index >= rowSize):
                            return False
                        cellValue = rowValues[index]
                        if cellValue == 0:
                            return False

                    if isLastBlock == False and index < rowSize-1:
                        index+= 1
                        cellValue = rowValues[index]
                        if cellValue == 1:
                            return False

                    blockIndex+=1

                if isLastBlock == True:

                    if index<rowSize - 1:

                        for k in range(index+1,rowSize):
                            cellValue = rowValues[k]
                            if cellValue == 1:
                                return False
                        print(number,rowValues,rowClue)
                        return True

                    else:
                        print (number,rowValues,rowClue)
                        return True

                index = index + 1
        print(number,rowValues,rowClue)
        return True

    def columnClueConstraint(self,variables,values):

        for elementIndex in range(0,len(variables)):

            number = self.parseNumberFromVariable(variables[elementIndex])

            columnSize = self.numberOfRows

            columnClue = self.columnConstraints[number]

            columnValues = values[elementIndex]

            numberOfBlocks = len(columnClue)

            blockIndex = 0

            isLastBlock = False

            blackCellNumber = 0

            for num in range(0,len(columnClue)):
                blackCellNumber = blackCellNumber + columnClue[num]

            realBlackCells = 0
            for num in range(0,len(columnValues)):
                if columnValues[num] == 1:
                    realBlackCells +=1

            if realBlackCells != blackCellNumber:
                return False

            index = 0

            while index < columnSize:
                lengthOfCurrentBlock = columnClue[blockIndex]
                cellValue = columnValues[index]

                if cellValue == 1:
                    if blockIndex == numberOfBlocks - 1:
                        isLastBlock = True

                    for j in range(0,lengthOfCurrentBlock -1 ):
                        index+=1
                        if(index >= columnSize):
                            return False
                        cellValue = columnValues[index]
                        if cellValue == 0:
                            return False

                    if isLastBlock == False and index < columnSize-1:
                        index+= 1
                        cellValue = columnValues[index]
                        if cellValue == 1:
                            return False

                    blockIndex+=1

                if isLastBlock == True:

                    if index < columnSize - 1:

                        for k in range(index+1, columnSize):
                            cellValue = columnValues[k]
                            if cellValue == 1:
                                return False
                        print(number,columnValues,columnClue)
                        return True

                    else:
                        print(number,columnValues,columnClue)
                        return True
                index = index + 1

        print(number, columnValues, columnClue)
        return True

    def clueConstraint(self,variables,values):

        isRow = False
        if self.parseRowIndexFromCell(variables[0]) == self.parseRowIndexFromCell(variables[1]):
            isRow = True

        dimensionIndex = None
        size = None
        clue = None

        if isRow == True:
            dimensionIndex = self.parseRowIndexFromCell(variables[0])
            clue = self.rowConstraints[dimensionIndex]
            size = self.numberOfColumns # row size = number of columns
        else:
            dimensionIndex = self.parseColumnIndexFromCell(variables[0])
            clue = self.columnConstraints[dimensionIndex]
            size = self.numberOfRows # column size = number of rows

        numberOfBlocks = len(clue)

        blackCellNumber = 0

        for num in range(0, len(clue)):
            blackCellNumber = blackCellNumber + clue[num]

        realBlackCells = 0

        for num in range(0, len(values)):
            if values[num] == 1:
                realBlackCells += 1

        if realBlackCells != blackCellNumber:
            return False

        blockIndex = 0

        isLastBlock = False

        index = 0

        while index < size:
            lengthOfCurrentBlock = clue[blockIndex]
            cellValue = values[index]

            if cellValue == 1:
                if blockIndex == numberOfBlocks - 1:
                    isLastBlock = True

                for j in range(0, lengthOfCurrentBlock - 1):
                    index += 1
                    if (index >= size):
                        return False
                    cellValue = values[index]
                    if cellValue == 0:
                        return False

                if isLastBlock == False and index < size - 1:
                    index += 1
                    cellValue = values[index]
                    if cellValue == 1:
                        return False

                blockIndex += 1

            if isLastBlock == True:

                if index < size - 1:

                    for k in range(index + 1, size):
                        cellValue = values[k]
                        if cellValue == 1:
                            return False
                    print(dimensionIndex, values, clue)
                    return True

                else:
                    print (dimensionIndex, values, clue)
                    return True

            index = index + 1

        print(dimensionIndex, dimensionIndex, clue)
        return True

    def parseNumberFromVariable(self,variable):
        if 'Row' in variable:
            if('Row 10' in variable or 'Column 10' in variable):
                number = 9
            else:
                number = int (variable[4]) - 1
        else:
            if('Column 10' in variable):
                number = 9
            else:
                number = int (variable[7]) - 1
        return number

    def parseRowIndexFromCell(self,variable):
        index = int(variable[4])
        return index

    def parseColumnIndexFromCell(self,variable):
        index = int(variable[5])
        return index




if __name__ == '__main__':
    PickPix().solve()


