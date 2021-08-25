class PiecewiseFunc(object):
    def __init__(self, step, value):
        self.__xMin = step[0]
        self.__xMax = step[-1]
        self.__steps = step
        self.__values = value
        self.__minValue = None

    def getSteps(self):
        return self.__steps

    def getValues(self):
        return self.__values

    # Get value of the function of a time point
    def getFuncValue(self, step):
        value = float("inf")
        for i in range(len(self.__steps)-1):
            if self.__steps[i] == step:
                value = self.__values[i]
            if self.__steps[i] < step and self.__steps[i+1] > step:
                value = self.__values[i]
        return value

    def setInterval(self, x1, x2):
        xMin = x1 
        xMax = x2
        
        steps = self.__steps[:]
        values = self.__values[:]

        if xMin < self.__xMin or xMax > self.__xMax:
            text = "Error: Min/Max value out of range"
            print(text)
            return text
        
        if xMin not in steps:
            for i in range(len(steps)):
                # check if x1 in steps, if not insert this point
                if steps[i] < xMin:
                    if xMin < steps[i+1]:
                        self.__steps.insert(i+1, xMin)
                        self.__values.insert(i+1, values[i])
                        break
                                                
        if xMax not in steps:
            for i in range(1, len(steps)+1):
                if steps[-i] > xMax:
                    if xMax > steps[-i-1]:
                        self.__steps.insert(-i, xMax)
                        self.__values.insert(-i, values[-i])
                        break
        
        steps = self.__steps[:]
        values = self.__values[:]        

        # print("Steps: {0}, values {1}".format(steps, values))
        
        # Remove points
        tempSteps = []
        tempValues = []
        for i in range(len(steps)):
            #print("step {0}: {1}".format(i, steps[i]))
            if steps[i] < xMin or steps[i] > xMax:
                continue
            
            tempSteps.append(steps[i])
            
            if steps[i] == xMax:
                continue
            tempValues.append(values[i])

        self.__steps = tempSteps[:]
        self.__values = tempValues[:]
        self.xMin = self.__steps[0]
        self.xMax = self.__steps[-1]

    def setFunc(self, step, value):
        self.__steps = step
        self.__values = value
        self.__xMin = step[0]
        self.__xMax = step[-1]

    def setValue(self, value):
        self.__values = value

    def addConstant(self, c):
        for i in range(len(self.__values)):
            self.__values[i] += c
    
    def shiftLeft(self, value):
        self.__xMin += value
        self.__xMax += value
        
        for i in range(len(self.__steps)):
            self.__steps[i] += value

    # Get min Value of the function within a domain
    def findMin(self, domain):
        func = PiecewiseFunc(self.__steps, self.__values)
        func.setInterval(domain.xMin, domain.xMax)
        self.__minValue = min(func.__values)
        return self.__minValue
    
    # Get min Time of a value
    def findTime(self, value):
        ind = self.__values.index(value)
        return self.__steps[ind]

    # Get min function of the two
    def minTwo(self, obj):
        resSteps = sorted(list(set(self.getSteps() + obj.getSteps())))
        #a = self.getValues()
        #b = obj.getValues()
        resValues = []
        for i in range(len(resSteps)-1):
            s = self.getFuncValue(resSteps[i])
            o = obj.getFuncValue(resSteps[i])
            if s < o:
                resValues.append(s)
            else:
                resValues.append(o)
        return PiecewiseFunc(resSteps, resValues)

class FuncDomain(object):
    def __init__(self, value1, value2):
        self.xMin = value1
        self.xMax = value2
    
    def __sub__(self, obj):
        if obj.xMin == 0 and obj.xMax == 0:
            return FuncDomain(self.xMin, self.xMax)
        
        if self.xMin == obj.xMin:
            return FuncDomain(obj.xMax, self.xMax)  
        elif self.xMax == obj.xMax:
            return FuncDomain(self.xMin, obj.xMin)
        else:
            return 0

    def addConstant(self, value):
        self.xMin += value
        self.xMax += value

    def __eq__(self, obj):
        return isinstance(obj, FuncDomain) and obj.xMin == self.xMin and obj.xMax == self.xMax

def test_func(args):
    f = PiecewiseFunc([1, 10, 30, 60], [2, 4, 3])
    print("Steps: {0}. Values: {1}".format(f.getSteps(), f.getValues()))

    # Test minTwo
    g = PiecewiseFunc([0, 5, 60], [1, 2])

    h = f.minTwo(g)
    print("MinTwo test with G...")
    print("G: Steps: {0}. Values: {1}".format(g.getSteps(), g.getValues()))
    print("Results: Steps: {0}. Values: {1}".format(h.getSteps(), h.getValues()))
    print("--------")
    
    f.setInterval(5, 25)
    #f.setInterval(5, 10)
    print("setInterval test...")
    print("Steps: {0}. Values: {1}".format(f.getSteps(), f.getValues()))
    print("--------")

    f.shiftLeft(10)
    print("shiftLeft test (10 units)...")
    print("Steps: {0}. Values: {1}".format(f.getSteps(), f.getValues()))
    print("--------")

    f.addConstant(10)
    print("addConstant (10 units) test...")
    print("Steps: {0}. Values: {1}".format(f.getSteps(), f.getValues()))
    print("--------")

    print("Min value: {0} at {1}".format(f.findMin(), f.findMinTime()))
    print("Time value of value of {0} at {1}".format(14, f.findTime(14)))