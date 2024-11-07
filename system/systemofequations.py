from sympy import * 
import sympy
from sympy.abc import a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z
import re
class SystemOfEquations:
  def __init__(self, equation_set):
    self.equation_set = equation_set
  def solvesystemthree(self):
    equationList = self.equation_set.split(",")
    equations = []
    for eq in equationList:
      equations.append(eq)
    equationFormat = []
    iterator = 0
    while iterator < len(equations):
      equationToAdd = []
      decompose = str(equations[iterator]).split("=")
      equationToAdd.append(decompose[0])
      equationToAdd.append(decompose[1])
      equationFormat.append(equationToAdd)
      iterator += 1
      
    #Remove white space
    iterator = 0
    while iterator < len(equationFormat):
      nestedIterator = 0
      while nestedIterator < len(equationFormat[iterator]):
        equationFormat[iterator][nestedIterator] = sympy.parsing.sympy_parser.parse_expr(equationFormat[iterator][nestedIterator], transformations="all")
     
        nestedIterator += 1
      iterator += 1

    #Solve system
    solutions = sympy.solve([sympy.Eq(equationFormat[0][0], equationFormat[0][1]), sympy.Eq(equationFormat[1][0], equationFormat[1][1]), sympy.Eq(equationFormat[2][0], equationFormat[2][1])], dict=True)
    return solutions

    
  def solvesystemtwo(self):
    equationList = self.equation_set.split(",")
    equations = []
    for eq in equationList:
      equations.append(eq)
    equationFormat = []
    iterator = 0
    while iterator < len(equations):
      equationToAdd = []
      decompose = str(equations[iterator]).split("=")
      equationToAdd.append(decompose[0])
      equationToAdd.append(decompose[1])
      equationFormat.append(equationToAdd)
      iterator += 1
      
    #Remove white space
    iterator = 0
    while iterator < len(equationFormat):
      nestedIterator = 0
      while nestedIterator < len(equationFormat[iterator]):
        equationFormat[iterator][nestedIterator] = sympy.parsing.sympy_parser.parse_expr(equationFormat[iterator][nestedIterator], transformations="all")
     
        nestedIterator += 1
      iterator += 1

    #Solve system
    solutions = sympy.solve([sympy.Eq(equationFormat[0][0], equationFormat[0][1]), sympy.Eq(equationFormat[1][0], equationFormat[1][1])], dict=True)
    return solutions
  def solvesystem(self):
    numberOfEquations = self.equation_set.count(",") + 1
    if numberOfEquations == 2:
      return self.solvesystemtwo()
    elif numberOfEquations == 3:
      return self.solvesystemthree()
    else:
      return "An error occured."

