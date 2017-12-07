from simpleai.search import CspProblem,convert_to_binary
from simpleai.search import backtrack,MOST_CONSTRAINED_VARIABLE,LEAST_CONSTRAINING_VALUE


class PickPix(object):
    def __init__(self):

        '''variables = ('A', 'B', 'C')

        domains = {
            'A': [1, 2, 3],
            'B': [1, 3],
            'C': [1, 2],
        }

        # a constraint that expects different variables to have different values
        def const_different(variables, values):
            print ('b')
            return len(values) == len(set(values))  # remove repeated values and count

        # a constraint that expects one variable to be bigger than other
        def const_one_bigger_other(variables, values):
            print ('a')
            return values[0] > values[1]

        # a constraint thet expects two variables to be one odd and the other even,
        # no matter which one is which type
        def const_one_odd_one_even(variables, values):
            print ('c')
            if values[0] % 2 == 0:
                return values[1] % 2 == 1  # first even, expect second to be odd
            else:
                return values[1] % 2 == 0  # first odd, expect second to be even

        constraints = [
            (('A', 'B', 'C'), const_different),
            (('A', 'C'), const_one_bigger_other),
            (('A', 'C'), const_one_odd_one_even),
        ]

        my_problem = CspProblem(variables, domains, constraints)

        result = backtrack(my_problem)'''

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

        #self.initializeEmptyRowsAndColumns()
        self.initializeVariables()
        self.variablesTuple = tuple(self.variables)


        self.makeRowDomain(0,[])
        self.makeColumnDomain(0,[])

        self.rows = self.getRows()
        self.columns = self.getColumns()

        self.rowsTuple = tuple(self.rows)
        self.columnsTuple = tuple(self.columns)

        self.initializeDomains()
        #self.initializeConstraints()




        print(self.variablesTuple)
        print(self.domains)
        #print(self.constraints)

        #rows tuple ve columns tuple ver

        self.constraints1 = [
            (self.variablesTuple, self.clueConstraint),
            (self.variablesTuple,self.rowColumnConsistency)
        ]


        #self.variablesTuple,self.domains,self.constraints1 = convert_to_binary(self.variablesTuple,self.domains,self.constraints1)

        problem = CspProblem(self.variablesTuple,self.domains,self.constraints1)

        result = backtrack(problem)

        print (result)



    def solve(self):
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

    def initializeEmptyRowsAndColumns(self):
        self.rows = []
        self.columns = []
        for rowIndex in range(0,self.numberOfRows):
            self.rows.append([])
        for columnIndex in range(0,self.numberOfColumns):
            self.columns.append([])


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

    '''def initializeConstraints(self):
        constraintList = []
        constraintList.append((self.variablesTuple,self.rowColumnConsistency))
        
        for i in range(0,self.numberOfRows):
            tupleRow = (self.rows[i],)
            constraintList.append((tupleRow,self.rowClueConstraint))

        for j in range(0,self.numberOfColumns):
            tupleColumn = (self.columns[j],)
            constraintList.append((tupleColumn,self.columnClueConstraint))

        rowsTuple = tuple(self.rows)
        constraintList.append((rowsTuple, self.rowClueConstraint))
        columnsTuple = tuple(self.columns)
        constraintList.append((columnsTuple, self.columnClueConstraint))

        self.constraints = constraintList
        return'''

    def rowColumnConsistency(self,variables,values):

        print('b')
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


            for index in range(0,rowSize):
                lengthOfCurrentBlock = rowClue[blockIndex]
                cellValue = rowValues[index]

                if cellValue == 1:
                    if blockIndex == numberOfBlocks - 1:
                        isLastBlock = True

                    for j in range(0,lengthOfCurrentBlock):
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


        return True

    def columnClueConstraint(self,variables,values):

        for elementIndex in range(0,len(variables)):

            print(" col")
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


            for index in range(0,columnSize):
                lengthOfCurrentBlock = columnClue[blockIndex]
                cellValue = columnValues[index]

                if cellValue == 1:
                    if blockIndex == numberOfBlocks - 1:
                        isLastBlock = True

                    for j in range(0,lengthOfCurrentBlock):
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


        return True

    def clueConstraint(self,variables,values):

        print('a')
        for elementIndex in range(0,len(variables)):

            number = self.parseNumberFromVariable(variables[elementIndex])

            size = self.numberOfColumns

            clue = None

            if 'Row' in variables[elementIndex]:
                clue = self.rowConstraints[number]
            else:
                clue = self.columnConstraints[number]

            dimensionValues = values[elementIndex]

            numberOfBlocks = len(clue)

            blackCellNumber = 0

            for num in range(0,len(clue)):
                blackCellNumber = blackCellNumber + clue[num]

            realBlackCells = 0

            for num in range(0,len(dimensionValues)):
                if dimensionValues[num] == 1:
                    realBlackCells +=1

            if realBlackCells != blackCellNumber:
                return False

            blockIndex = 0

            isLastBlock = False


            for index in range(0,size):
                lengthOfCurrentBlock = dimensionValues[blockIndex]
                cellValue = dimensionValues[index]

                if cellValue == 1:
                    if blockIndex == numberOfBlocks - 1:
                        isLastBlock = True

                    for j in range(0,lengthOfCurrentBlock):
                        index+=1
                        if(index >= size):
                            return False
                        cellValue = dimensionValues[index]
                        if cellValue == 0:
                            return False

                    if isLastBlock == False and index < size-1:
                        index+= 1
                        cellValue = size[index]
                        if cellValue == 1:
                            return False

                    blockIndex+=1


        return True


    def parseNumberFromVariable(self,variable):
        if 'Row' in variable:
            number = int (variable[4]) - 1
        else:
            number = int (variable[7]) - 1
        return number




if __name__ == '__main__':
    PickPix().solve()


