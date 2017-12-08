from simpleai.search import CspProblem,convert_to_binary
from simpleai.search import backtrack,MOST_CONSTRAINED_VARIABLE,LEAST_CONSTRAINING_VALUE


class PickPix(object):
    def __init__(self):

        self.countColumn = 0
        self.countRow = 0

        self.numberOfColumns = None  # equals to row size
        self.numberOfRows = None # equals to column size

        self.rowConstraints = []
        self.columnConstraints = []

        self.constraints = []
        self.readConstraintsFromFile()

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

        '''result = backtrack(problem,variable_heuristic=MOST_CONSTRAINED_VARIABLE,
                   value_heuristic=LEAST_CONSTRAINING_VALUE)'''

        result = backtrack(problem)

        print (result)


    def solve(self):
        print ('asd')
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

    def parseRowIndexFromCell(self,variable):
        index = int(variable[4])
        return index

    def parseColumnIndexFromCell(self,variable):
        index = int(variable[5])
        return index




if __name__ == '__main__':
    PickPix().solve()


