goodInputs = ['1', '2', '3', '4' , '5', '6', '7', '8', '9', '0', '.', '(', ')', '/', "*", "^", "+", "-"]
numberList = ['1', '2', '3', '4' , '5', '6', '7', '8', '9', '0']
def calculate(expression):
    calculationList = []
    for x in expression:
        if x in goodInputs:
            pass
        else:
            return "An error occured."
    icounter = 0
    for x in expression:
        calculationList.append(x)
    while icounter <= len(expression) - 1:
        if icounter != len(expression) - 1 and (calculationList[icounter] in numberList and calculationList[icounter + 1] == "("):
            calculationList.insert(icounter + 1, "*")
        icounter += 1
    expression = ""
    for x in calculationList:
        expression += x
    try:
        result = eval(str(expression))
        return result
    except:
        return "An error occured."