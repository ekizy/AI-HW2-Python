from simpleai.search import CspProblem

class PickPix(object):
    def __init__(self):
        variables1 = ('rows', 'columns')
        domains = {'Rows'}
        self.numberOfColumns = None
        self.numberOfRows = None
        self.rowConstraints = []
        self.columnConstraints = []
        self.variables = None
        self.domains = None
        self.readConstraintsFromFile()

        print(self.rowConstraints)
        print(self.columnConstraints)

        self.initializeVariables()
        self.initializeDomains()
        print(self.domains)
        #self.initializeConstraints()

    def solve(self):
        print('asd')

    def const_row(self,variables,values):
        print ('asd')

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
        variablesString = '('
        for rowIndex in range(0,self.numberOfRows):
            for columnIndex in range(0,self.numberOfColumns):
                variablesString = variablesString + 'Cell '+ str(rowIndex+1)+ str(columnIndex+1)
                if rowIndex == self.numberOfRows - 1 and columnIndex == self.numberOfColumns - 1:
                    variablesString = variablesString + ')'
                else:
                    variablesString = variablesString + ','
        self.variables = variablesString

    def initializeDomains(self):
        allVariables = self.variables.replace("(","").replace(")","").split(",")
        domainsString = '{'
        for index in range(0,len(allVariables)):
            variableName = allVariables[index]
            tempDomainString = variableName + ': ["#",""],'
            domainsString = domainsString + tempDomainString
            if index == len(allVariables) -1:
                domainsString = domainsString + "}"
        self.domains = domainsString


if __name__ == '__main__':
    PickPix().solve()


