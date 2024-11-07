import nextcord
from random import choice

class Quiz:
  def __init__(self, question=None, a=None, b=None, c=None, d=None, correct_answer=None):
    self.question = question
    self.a = a
    self.b = b
    self.c = c
    self.d = d
    self.correct_answer = correct_answer
  
  def check_answer(self, userAnswer):
    if userAnswer == self.correct_answer:
      return True
    else:
      return False
class Question:
  def __init__(self, question, options, correct_answer):
    self.question = question
    self.options = options
    self.correct_answer = correct_answer

class Quiz:
  def __init__(self, question_bank):
    self.question_bank = question_bank
  def sendquiz(self):
    question = choice(self.question_bank)
    text = ""
    i = 1
    for option in question.options:
      text += f"{i}) {option}\n"
      i += 1
    embed = nextcord.Embed(
      title = f"{question.question}",
      description = text,
      color = 0x0736e0,
    )
    embed.set_footer(text=f"Question #{self.question_bank.index(question) + 1}")
    return embed, question.options, question.correct_answer
    
questions = [
  Question("Let f(x, y) = (x, y). Find ∇f", ["(1, 1)", "(0.5x^2, 0.5y^2)", "(y, x)", "(0, 0)"], 1),
  Question("Compute ∫ (2x/(x^2)) dx", ["2x + C", "ln(x^2) + C", "x^2 + C", "(2(x^2) - 4x^2)/x^4 + C"], 2),
  Question("Which of the following is not a town in Southern California?", ["Zzyzx", "Seattle", "Big Bear Lake", "None of the above"], 2),
  Question("Which of the following is not a town in Southern California?", ["Zzyzx", "Seattle", "Big Bear Lake", "None of the above"], 2),
  Question("Air is mainly composed of", ["Oxygen", "Nitrogen", "Carbon", "Sulfur"], 2),
  Question("What is the approximate distance around the equator of Earth?", ["40074 km", "3422 km", "2342 km", "9.8 km"], 1),
  Question("Which of the following is an equivalent form of (e^x)(e^x)?", ["e^(2x)", "2e^x", "e^(x^2)", "None of the above"], 1),
  Question("Which of the following elements is radioactive?", ["Thulium", "Thallium", "Thorium", "Nitrogen"], 3),
  Question("Compute the second derivative with respect to x of 5x^4.", ["20x^3", "60x^2", "120x", "120"], 2),
  Question("Approximately how many seconds are in one day?", ["1", "60", "3600", "86400"], 4),
  Question("Generally, going across a period on the periodic table from left to right, each successive element will have a _ atomic radius than the previous.", ["Equal", "Smaller", "Larger", "rougher"], 2),
  Question("In Star Wars, Luke Skywalker is:", ["A cow", "Anakin's Son", "Yoda's Cousin", "Anakin's father"], 2),
  Question("The speed of light is commonly denoted as the letter:", ["a", "b", "c", "d"], 3),
  Question("Which group of the periodic table contains the most reactive nonmetals?", ["Noble Gases", "Akali Metals", "Alkaline Earth Metals", "Halogens"], 4),
  Question("Determine the momentum of a 10 kg object moving at velocity 5î+3ĵ m/s.", ["50î+30ĵ kg m/s", "0.5î+0.3ĵ kg m/s", "50î+30ĵ kg ft/s", "None of the above"], 1),
  Question("In the movie Back to the Future, how much power is needed for the time machine to work?", ["1.65 GW", "9 GW", "88 GW", "1.21 GW"], 4),
  Question("Determine the equation of a circle centered at (5, 2) on the xy plane, with radius 2.", ["(x-5)^2 + (x-2)^2 = 4", "(x+5)^2 + (y+2)^2 = 4", "(x+5) + (y+2) = 4", "None of the above"], 1),
  Question("Which of the following is considered to be a drupe in botany?", ["Strawberry", "Coconut", "Watermelon", "Pomegranate"], 2),
  Question("ln(4x)=", ["ln(4) + ln(x)", "ln(4) - ln(x)", "4ln(x)", "None of the above"], 1),
  Question("What is the range of the function g(x) = ln(x+1)?", ["(-∞, ∞)", "(0, ∞)", "(-1, ∞)", "[0, ∞)"], 1),
  Question("Let f(x,y) = (x^2)(e^y). Find ∂f/∂x", ["(e^y)(x^2)", "2xe^y", "(x^2)(e^y) + (2x)(e^y)", "None of the above"], 2),
  Question("log(x)=", ["ln(x)", "ln(10) + ln(x)", "ln(x)/ln(10)", "ln(10) - ln(x)"], 3),
  Question("Find the y-intercept of the graph y=e^5x", ["(1, 0)", "(5, 0)", "(e, 5)", "(0, 1)"], 4),
  Question("What is the range of y=-e^x?", ["(0, ∞)", "(-∞, ∞)", "(-∞, 0)", "[0, ∞)"], 3),
  Question("Let a = (0, 4, 5) and b = (0, 3, 2). Compute a • b.", ["22", "0", "Undefined", "None of the above"], 1),
  Question("About how many miles long is interstate 82 in the United States?", ["143.58mi", "500mi", "26.2mi", "Interstate 82 does not exist."], 1),
  Question("Sequoia National Park in California of the United States has an area of approximately: ", ["5280 acres", "360 acres", "404,064 acres", "406,890 acres"], 3),
  Question("Let f(x)=x^e. Find df/dx", ["ex^(e-1)", "e", "x^(e+1)", "None of the above"], 1),
  Question("About how many km squared is the island of Svalbard?", ["61023km^2", "61022km^2", "1km^2", "None of the above"], 1),
  Question("Uturuncu, a volcano in Bolivia, is approximately how tall in meters?", ["9400m", "1000m", "6008m", "5280m"], 3),
  Question("Suppose h(x) = e^(2x-3). What is the range of this function?", ["(0, ∞)", "(-∞, ∞)", "(-∞, 0)", "[0, ∞)"], 1),
  Question("Compute ∫e^(2x) dx", ["2e^(2x) + C", "(1/2)e^(2x) + C", "e^(2x) + C", "ln(2x) + C"], 2),
  Question("The charge in a certain wire is modeled by the function Q(t)=e^(-2t). Find the current in the wire as a function of time.", ["I(t) = (-1/2)e^(-2t)", "I(t) = e^(-2t)", "I(t) = -2e^(-2t)", "I(t) = -2t"], 3),
  Question("A certain series circuit has a voltage source of 5V, with an equivalent resistance of 10 ohms. Find the current in the circuit.", ["I = 2A", "I = 50A", "I = 0A", "I = 0.5A"], 4),
  Question("A certain AC circuit has a maximum voltage of 10V, and a frequency of 3Hz with no phase shift. Determine the expression for the voltage in the circuit as a function of time.", ["v(t) = 3sin(10t)", "v(t) = 3sin(10πt)", "v(t) = 10sin(3t)", "v(t) = 10sin(6πt)"], 4),
  Question("Haribo, the confectionary company, is currently based in", ["Sweeden", "Germany", "Atlantic Ocean", "Denmark"], 2),
  Question("Lines that are perpendicular to each other intersect to form:", ["Acute angles", "Right angles", "Obtuse angles", "Try angles"], 2),
  Question("Alice is located at point A or point B, and not located at the same place as Bob. Bob is located at point B. What point is Alice located at?", ["B", "Cannot be determined", "D", "A"], 4),
  Question("A certain wave has a wavelength of 5m and a frequency of 10Hz. Find the speed of the wave.", ["50 m/s", "4 m/s", "0.02 m/s", "20 m/s"], 1),
  Question("The leader of a herd of elephants is called the", ["matriarch", "boss", "pride", "trunk"], 1),
  Question("One interior angle of an equilateral triangle is equal to:", ["60 degrees", "90 degrees", "180 degrees", "None of the above"], 1),
  Question("The compound MgO is an example of a(n)", ["Molecular compound", "Metallic compound", "Compound sentence", "Ionic compound"], 4),
  Question("Compute ∫sin(2x) dx", ["cos(2x)/2 + C", "sin(2x)/2 + C", "-cos(2x)/2 + C", "sin(2x) + C"], 3),
  Question("Independence day for Argentina is", ["July 9", "January 31", "April 3", "October 31"], 1),
  Question("The cheetah is native to which of the following areas?", ["Central Iran and Africa", "Atlantic and Pacific oceans", "Norway and Iceland", "None of the above"], 1),
  Question("Which of the following group one elements of the periodic table is not a metal?", ["Fr", "H", "Li", "All of the above are metals"], 2),
  Question("How many keys does a standard piano have?", ["900 keys", "88 keys", "35 keys", "5 keys"], 2),
  Question("The equation of circle C is (x-3)^2 + (y-4)^2 = 36. What is the radius of the circle?", ["8", "7", "6", "None of the above"], 3),
  Question("The elements on the periodic table were originally ordered by", ["Atomic number", "Number of electrons", "Atomic Mass", "Color"], 3),
  Question("In terms of computing, SMTP stands for:", ["Simple mail transfer protocol", "Standard mailing turtle procedure", "Static mail transfer programming", "Standard market tuna price"], 1),
  Question("Compute the derivative with respect to x of sin(2x)", ["2sin(2x)", "2cos(2x)", "0.5sin(2x)", "-0.5cos(2x)"], 2),
  Question("Compute the derivative with respect to t of e^(5t^2)", ["10te^(5t^2)", "e^(5t^2)", "e", "10t"], 1),
  Question("Let v(x, y) = (5sin(x), 5y). Compute ∇•v", ["-5cos(x) + 5", "5sin(x) + 5y", "5cos(x) + 5", "None of the above"], 3),
  Question("Let v(x, y) = (5sin(x), 5y). Compute ∇•v", ["-5cos(x) + 5", "5sin(x) + 5y", "5cos(x) + 5", "None of the above"], 3),
  Question("Who was the first president of the United States?", ["George Washington", "John Adams", "Thomas Jefferson", "James Madison"], 1),
  Question("The mole, a unit in chemistry is commonly abbreviated as", ["mol", "moo", "m", "mo"], 1),
  Question("The scientific definition of power is", ["mass times acceleration", "mass times speed of light", "work over time", "elephants"], 3),
  Question("The name \"Polaris\", is a modern shortened name from the new latin name of", ["stella", "polaris stella", "stella polaris", "None of the above"], 3),
  Question("Which group one element of the periodic table is not a metal?", ["He", "H", "Li", "Fr"], 2),
  Question("Helium, the element is a", ["Halogen", "Akali metal", "Alkaline metal", "Noble gas"], 4),
  Question("As you go up a given group on the periodic table, the ionization energy of an element", ["Increases", "Stays the same", "Decreases", "None of the above"], 1),
  Question("Group two of the periodic table is commonly referred to as", ["Alkali metals", "Halogens", "Noble Gases", "Alkaline Earth Metals"], 4),
  Question("Which experiment also is credited to be the discovery of the electron?", ["Cathode ray tube", "Gold Foil Experiment", "Flame Test", "None of the above"], 1),
  Question("Which of the following is not considered to be a fundamental force between particles?", ["Gravity", "Electromagnetism", "Weak Nuclear Force", "Ionization Energy"], 4),
  Question("Nerds, the candy, were first launched in what year?", ["1776", "1883", "1983", "2016"], 3),
  Question("When chlorine forms an ionic bond with another element, it is most likely to form a", ["Anion", "Cation", "Electron", "Nucleus"], 1),
  Question("The nucleus of an atom has a", ["Positive charge", "Negative Charge", "No charge", "None of the above"], 1),
  Question("How many numbers are prime numbers from 1 to 10, not including 1 and 10?", ["4", "3", "15", "2"], 2),
  Question("1 joule, the unit of energy, is equal to", ["1 m/s", "1kg", "1 N * m", "None of the above"], 3),
  Question("Following the octet rule, oxygen in its stable ionic form, has a charge of", ["+1", "-1", "+2", "-2"], 4),
  Question("Haribo, the confectionery company, is currently based in", ["Sweden", "Germany", "Atlantic Ocean", "France", "Denmark"], 2),
  Question("An bisector of a given angle:", ["Divides the given angle into two congruent angles", "Is equal to twice the amount of the given angle", "Adds up to 180 degrees", "None of the above"], 1),
  Question("Angles of a triangle add up to:", ["360 degrees", "90 degrees", "180 degrees", "190 degrees"], 3),
  Question("The measure of one exterior angle of a regular polygon with n sides is equal to:", ["180n-2", "360/n", "360/(n-2)", "None of the above"], 2),
  Question("43 is a prime number.", ["True", "False", "Partially True", "Both true and false"], 1),
  Question("Which of the following compounds is not created through ionic bonds (Any numbers in answer choices are meant to be subscripts)?", ["H2O", "NaCl", "LiF", "NiO"], 1),
  Question("An Airbus 380, the airplane, has __ engines:", ["11", "3", "15", "4"], 4),
  Question("If hydrogen bonds with oxygen, the hydrogen ions will be:", ["Anions", "Cations", "Water", "Atoms"], 2),
  Question("The number 1500 has __ significant figures:", ["0", "3", "2", "23234"], 3),
  Question("Lines that are perpendicular to each other intersect to form:", ["Acute angles", "Right angles", "Obtuse angles", "Try angles"], 2),
  Question("The hypotenuse of a right triangle is:", ["the longest side of the triangle", "The shortest side of the triangle", "Invisible", "Located in the Atlantic Ocean"], 1),
  Question("A square has:", ["Four congruent sides", "Four acute interior angles", "No sides", "No angles"], 1),
  Question("Any rhombus is also a:", ["Square", "Parallelogram", "Circle", "Triangle"], 2),
  Question("All rectangles are", ["Parallelograms", "Circles", "Triangles", "congruent"], 1),
  Question("Independence day for Argentina is", ["July 9", "January 31", "April 3", "October 31"], 1),
  Question("In terms of computing, SMTP stands for:", ["Simple mail transfer protocol", "Standard mailing turtle procedure", "Static mail transfer programming", "Standard market tuna price"], 1),
  Question("Which of the following is not a triangle congruence postulate?", ["SSS", "SAS", "EGG", "None of the above"], 3),
  Question("Given the function f(x) = x^2, what is the output when x = 3?", ["3", "5", "9", "15"], 3),
  Question("The leader of a herd of elephants is called the", ["matriarch", "boss", "pride", "trunk"], 1),
  Question("As square is a __ with four congruent sides.", ["Rectangle", "Rhombus", "Circle", "Triangle"], 1),
]  

"""










q43 = Quiz("43 is a prime number.", "1 [True]\n2 [False]\n3 [Partially True]\n4 [Both true and false]", "1️⃣")

q45 = Quiz("Which of the following compounds **is not** created through ionic bonds (Any numbers in answer choices are meant to be subscripts)? ", "1 [H2O]\n2 [NaCl]\n3 [LiF]\n4 [NiO]", "1️⃣")
q46 = Quiz("An Airbus 380, the airplane, has __ engines: ", "1 [11]\n2 [3]\n3 [15]\n 4 [4]", "4️⃣")
q47 = Quiz("If hydrogen bonds with oxygen, the hydrogen ions will be: ", "1 [Anions]\n2 [Cations]\n 3 [Water]\n4 [Atoms]", "2️⃣")
q48 = Quiz("The number 1500 has __ significant figures: ", "1 [0]\n2 [3]\n3 [2]\n4 [23234]", "3️⃣")
q49 = Quiz("Lines that are perpendicular to each other intersect to form: ", "1 [Acute angles]\n2 [Right angles]\n3 [Obtuse angles]\n4 [Try angles]", "2️⃣")
q50 = Quiz("The hypotenuse of a right triangle is: ", "1 [the longest side of the triangle]\n2 [The shortest side of the triangle]\n3 [Invisible]\n4 [Located in the Atlantic Ocean]", "1️⃣")
q51 = Quiz("A square has: ", "1 [Four congruent sides]\n2 [Four acute interior angles]\n3 [No sides]\n4 [No angles]", "1️⃣")
q52 = Quiz("Any rhombus is also a: ", "1 [Square]\n2 [Parallelogram]\n3 [Circle]\n 4 [Triangle]", "2️⃣")
q54 = Quiz("All rectangles are ", "1 [Parallelograms]\n2 [Circles]\n3 [Triangles]\n4 [congruent]", "1️⃣")

q56 = Quiz("Independence day for Argentina is ", "1 [July 9]\n2 [January 31]\n3 [April 3]\n4 [October 31]", "1️⃣")
q57 = Quiz("In terms of computing, SMTP stands for: ", "1 [Simple mail transfer protocol]\n 2 [Standard mailing turtle procedure]\n3 [Static mail transfer programming]\n4 [Standard market tuna price]", "1️⃣")
q58 = Quiz("Which of the following is **not** a triangle congruence postulate?", "1 [SSS]\n2 [SAS]\n 3[EGG]\n4[None of the above]", "3️⃣")
q59 = Quiz("Given the function f(x) = x^2, what is the output when x = 3?", "1 [3]\n2 [5]\n3 [9]\n4 [15]", "3️⃣")
q60 = Quiz("The leader of a herd of elephants is called the ", "1 [matriarch]\n2 [boss]\n 3 [pride]\n4 [trunk]", "1️⃣")
q61 = Quiz("As square is a __ with four congruent sides.", "[1 [Rectangle]\n2 [Rhombus]\n 3 [Circle]\n 4[Triangle]", "1️⃣")
q62 = Quiz("As the concentration of H+ ions in a solution increases, the pH of the solution: ", "1 [Increases]\n2 [Decreases]\n3 [Remains Constant]\n4 [None of the above]", "2️⃣")
q63 = Quiz("Bob pushes on an object with a force. He then pushes an identical object with twice the force. This object will have: ", "1 [Twice the acceleration]\n2 [1/2 the acceleration]\n3 [The same acceleration]\n4 [No acceleration]", "1️⃣")
q64 = Quiz("Alice is located at point A or point B, and not located at the same place as Bob. Bob is located at point B. What point is Alice located at?", "1 [B]\n2 [Cannot be determined]\n 3 [D]\n 4 [A]", "4️⃣")
q65 = Quiz("The midpoint of a segment with endpoints (0, 6) and (6, 0) is:", "1 (0, 0)\n2 (0, 6)\n3 (3, 3)\n4 (6, 6)", "3️⃣")
q66 = Quiz("Element X has a half life of 6 days. After 6 days, how much of a 10g sample of element X be left?", "1 [10g]\n2 [0g]\n3 [5g]\n 4[None of the above]", "3️⃣")
q67 = Quiz("The slope of the line y=3 is", "1 [0]\n2 [undefined]\n3 [3]\n4 [None of these]", "1️⃣")
q68 = Quiz("The moment of inertia(I) of a rod with mass m and length r rotating about its center is:", "1 [1/12 mr^2]\n2 [mr^2]\n3 [1/3 mr^2]\n4 [None of the above]", "1️⃣")
q69 = Quiz("A 45-45-90 triangle has a hypotenuse of length 5sqrt(2). The length of the side adjacent to the hypotenuse is:", "1 [5]\n2 [6]\n3 [10]\n4 [None of the above]", "1️⃣")
q70 = Quiz("The equation of circle C is (x-3)^2 + (y-4)^2 = 36. What is the radius of the circle?", "1 [8]\n2 [7]\n3 [6]\n4 [None of the above]", "3️⃣")
q71 = Quiz("Given the following equations: y=3x+2\nx=2\nWhat is the value of y?", "1 [8]\n2 [16]\n3 [32]\n4 [0]", "1️⃣")
q72 = Quiz("The y intercept of the line y=5x+6 is", "1 [4]\n2 [3]\n3 [6]\n4 [18]", "3️⃣")
q73 = Quiz("A line with the equation x = 2 has a slope that is", "1 [2]\n 2 [Undefined]\n3 [6]\n4 [None of the above]", "2️⃣")
q74 = Quiz("Angle B is drawn in circle O with the endpoints of the angle touching the diameter of the circle. The measure of this angle is", " 1 [90 degrees]\n2 [360 degrees]\n3 [180 degrees]\n4 [45 degrees]", "1️⃣")
q75 = Quiz("A dilation is performed on line A centered at the origin.. Which of the following properties of the line remain the same after such a transformation?", "1 [slope]\n2 [y-intercept]\n3 [slope and y intercept]\n4 [None of the above]", "1️⃣")
q76 = Quiz("What is the theoretical probability that a 1 will be rolled on a 6 sided die?", "1 [1/6]\n 2[1/36]\n3 [1/3]\n4 [None of the above]", "1️⃣")
q77 = Quiz("Which of the following reactions results in lighter nuclei combining to form a heavier nucleus?", "1 [Nuclear fission]\n2 [Synthesis]\n3 [Nuclear fusion]\n4 [Combustion]", "3️⃣")
q78 = Quiz("What is the volume of cube with side length 5?", "1 [25]\n2 [5]\n3 [12.5]\n4 [125]", "4️⃣")
q79 = Quiz("Two sides of triangle ABC are of lengths 5 and 2 respectively. Which of the following measures can the third side **not** be?", "1 [4]\n2 [7]\n3 [3.5]\n4 [3.4]", "2️⃣")
q80 = Quiz("Triangle ABC is similar to triangle DEF. Which of the following pairs of ratios are not equivalent?", "1 [AB/DE and BC/EF]\n2 [CB/FE and BA/ED]\n3 [AC/DF and BC/EF]\n4 [AC/DE and FE/CB]", "4️⃣")
q81 = Quiz("How many keys does a standard piano have?", "1 [88 keys]\n2 [35 keys]\n3 [5 keys]\n4 [900 keys]", "1️⃣")
q82 = Quiz("What restrictions does the domain of the function y=(x-5)/(x+5) have?", "1 [x≠3]\n2 [x≠5]\n3 [x≠-5]\n4 [There are no restrictions on the domain.", "3️⃣")
q82 = Quiz("If f(x)=x, what is the inverse of f(x), g(x)?", "1 [g(x)=x]\n2 [g(x)=x^2]\n3 [g(x)=1]\n4 [None of the above]", "1️⃣" )
q83 = Quiz("Which expression is equivalent to ln(a)-ln(b)?", "1 [ln(a-b)]\n2 [ln(b-a)]\n3 ln[(a/b)]\n4 [ln(b/a)]", "3️⃣")
q84= Quiz("A substance changes from a gas to a solid. This process is known as", "1 [Sublimation]\n2 [Deposition]\n 3 [Evaporation]\n4 [Condensation]", "2️⃣")
q85 = Quiz("The Buckeye chicken was created in which American state?", "1 [Hawaii]\n2 [Minnesota]\n3 [New Jersey]\n4 [Ohio]", "4️⃣")
q86 = Quiz("Find the roots of the function h(x)=(x^2)+5x+6", "1 [x=-3, x=-2]\n2 [x=3, x=2]\n3 [x=0, x=1]\n4 [None of the above]", "1️⃣")
q87 = Quiz("How many meters are in 1 nm?", "1 [1*10^3 m]\n2 [1*10^6 m]\n3 [1*10^-9 m]\n4 [1*10^-2 m]", "3️⃣")
q88 = Quiz("A 9V battery is connected to a 3 ohm resistor in a closed circuit loop. What is the current flowing through the circuit?", "1 [27A]\n2 [3A]\n3 [14A]\n4 [None of the above]", "2️⃣")
q89 = Quiz("Find the rest energy of an object with mass 5kg.", "1 [5c^2 J]\n2 [5c J]\n3 [0 J]\n 4 [None of the above]", "1️⃣")
q90 = Quiz("Find the proper time interval for a spacecraft observed to travel for 5 seconds with a lorentz factor of 2.", "1 [2.5s]\n2 [10s]\n3 [25s]\n4 [None of the above]", "1️⃣")
q91 = Quiz("Find the speed of a car moving at 3î-4ĵ mph.", "1 [7 mph]\n2 [8 mph]\n3 [5 mph]\n4 [None of the above]", "3️⃣")
q92 = Quiz("What is the derivation of e^x?", "1 [e]\n2 [e^x]\n3 [e^0]\n4 [None of the above]", "2️⃣")
q93 = Quiz("What is ln(e)?", "1 [e]\n2 [1]\n3 [0]\n4 [None of the above]", "2️⃣")
q94 = Quiz("Boiling point of water at STP is approximately", "1 [100°C]\n2 [0°C]\n3 [1°C]\n4 [200°C]", "1️⃣")
q95 = Quiz("Which body of water contains the Mariana Trench?", "1 [Atlantic Ocean]\n2 [Pacific Ocean]\n3 [Columbia River]\n4 [None of the above]", "2️⃣")
q96 = Quiz("Which state is the fourth largest by area?", "1 [California]\n2 [Texas]\n3 [Alaska]\n4 [Montana]", "4️⃣")
q97 = Quiz("Approximately how tall is the Eiffel Tower?", "1 [200m]\n2 [300m]\n3 [400m]\n4 [500m]", "2️⃣")
q98 = Quiz("What is sin(π)?", "1 [0]\n2 [1]\n3 [-1]\n4 [None of the above]", "1️⃣")
q99 = Quiz("In what year was the original Star Wars film released?", "1 [2019]\n2 [1534]\n3 [1933\n4 [1977]", "4️⃣")
q100 = Quiz("Compute ∫e^x dx.", "1 [e^x + C]\n2 [e + C]\n3 [0]\n4 [None of the above]", "1️⃣")
q101 = Quiz("Evaluate ∫(2x/x^2)dx", "1 [2x + C]\n2 [x + C]\n3 [ln|x^2| + C]\n4 [None of the above]", "3️⃣")
q102 = Quiz("Which of the following is a solution to the equation cos(x) = 0?", "1 [kπ/2, k=1,3,5,7,...]\n2 [0k, k=1,2,3,4,...]\n3 [No solutions exist]\n4 [None of the above]", "1️⃣")
q103 = Quiz("Two identical springs perform oscillatory motion. Spring A has maximum displacement A, and Spring B has maximum displacement 2A. The total energy of spring B is __ times that of spring A", "1 [2]\n2 [0.5]\n3 [1]\n4 [4]", "4️⃣")
q104 = Quiz("The general solution to the differential equation (dy/dx)=2x is", "1 [y=x^2 + k]\n2 [y=ln(2x) + k]\n3 [No solution exists]\n4 [None of the above]", "1️⃣")
q105 = Quiz("A 5cm string has a fundemental frequency with wavelength", "1 [5cm]\n2 [10/3 cm]\n3 [10 cm]\n4 [None of the above]", "3️⃣")
q106 = Quiz("A particle executes uniform circular motion around a path with radius 3 meters. If the particle moves at a speed of 3 m/s, what is the magnitude of its centripetal acceleration?", "1 [3 m/s/s] 2 [9 m/s/s]\n3 [4 m/s/s]\n4 [None of the above]", "1️⃣")
q107 = Quiz("Expand (x+2)^2", "1 [(x^2)-4x+4]\n2 [(x^2)+4x+4]\n3 [Cannot be determined]\n4 [None of the above]", "2️⃣")
q108 = Quiz("Determine the kinetic energy of a 10kg car moving at 3 m/s.", "1 [30J]\n2 [100J]\n3 [45J]\n4 [90J]", "3️⃣")
q109 = Quiz("What is ln(e)?", "1 [1]\n2 [e]\n3 [1/e]\n4 [0]", "1️⃣")
q110 = Quiz("Object A moves at speed v. Object B moves at speed 2v. The kinetic energy of object B is _ times the kinetic energy of object A.", "1 [2]\n2 [1/2]\n3 [1]\n4 [4]", "4️⃣")
q111 = Quiz("Determine the velocity of a particle whose position in meters is described by the function s(t)=2t", "1 [1 m/s]\n2 [2 m/s]\n3 [4 m/s]\n4 [Cannot be determined]", "2️⃣")
q112 = Quiz("Consider the function f(x)=x. Find the inverse function, g(x).", "1 [g(x)=1]\n2 [g(x)=1/x]\n3 [g(x)=x]\n4 [g(x)=x^2]", "3️⃣")
q113 = Quiz("Find the vertex of the graph described by the function f(x) = (x-3)^2+6", "1 [(3,6)]\n2 [(3,-6]\n3 [(-3,6)]\n4 [(-3,-6)]", "1️⃣")
q114 = Quiz("2ln(a)=_", "1 [ln(2a)]\n2 [ln(a^2)]\n3 [ln(a/2)]\n4 [None of the above]", "2️⃣")
q115 = Quiz("Find |3i+4|", "1 [9]\n2 [16]\n3 [12]\n4 [5]", "4️⃣")
"""

#quizQuestionList = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24, q25, q26, q27, q28, q29, q30, q31, q32, q33, q34, q35, q36, q37, q38, q39, q40, q41, q42, q43, q44, q45, q46, q47, q48, q49, q50, q51, q52, q53, q54, q55]
