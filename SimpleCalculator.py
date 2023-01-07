from tkinter import *
from decimal import *
from sys import platform
if platform == "darwin": from tkmacosx import Button


class calculationParsers:
    def __init__(self):
        pass

    def start(self, equation: str):
        #parse by operators
        listedEquation = self.opSeperatorParser([equation], "÷")
        listedEquation = self.opSeperatorParser(listedEquation, "x")
        listedEquation = self.opSeperatorParser(listedEquation, "+")
        listedEquation = self.opSeperatorParser(listedEquation, "-")

        #check syntax
        syntaxFlag = self.syntaxParser(listedEquation)

        if syntaxFlag == True:
            #operation calculaton parsers
            listedEquation = self.opCalcParser(listedEquation, "÷")
            listedEquation = self.opCalcParser(listedEquation, "x")
            listedEquation = self.opCalcParser(listedEquation, "+")
            listedEquation = self.opCalcParser(listedEquation, "-")

            calcOutput = listedEquation[0]

            #result processer
            calcOutput = self.resultPorcesser(calcOutput)
        else:
            calcOutput = "Syntax Error"

        return calcOutput
    
    def opSeperatorParser(self, listedEquation: list, operator: str):
        parsedEquation = []
        for item in listedEquation:
            selectionStartIndex = 0
            for i in range(len(item)):
                if item[i] == operator:
                    parsedEquation.append(item[selectionStartIndex:i])
                    selectionStartIndex = i + 1
                    parsedEquation.append(operator)
            parsedEquation.append(item[selectionStartIndex:len(item) + 1])

        return parsedEquation

    def syntaxParser(self, listedEquation: list):
        if "" in listedEquation:
            return False
        for item in listedEquation:
            if item.isnumeric() == False and item.count(".") > 1 and (item in ["÷", "x", "+", "-"]) == False:
                return False
        return True

    def opCalcParser(self, listedEquation: list, operator: str):
        if listedEquation != "Math Error":
            i = 0
            while i < len(listedEquation):
                if listedEquation[i] == operator:
                    number1 = Decimal(listedEquation[i - 1])
                    number2 = Decimal(listedEquation[i + 1])
                    if operator == "÷" and number1 != 0:
                        result = number1 / number2
                    elif operator == "x":
                        result = number1 * number2
                    elif operator == "+":
                        result = number1 + number2
                    elif operator == "+":
                        result = number1 - number2
                    else:
                        return "Math Error"
                    del listedEquation[i - 1: i + 2]
                    listedEquation.insert(i, str(result))
                else:
                    i += 1

        return listedEquation

    def resultPorcesser(self, number: str):
        floatNum = float(number)

        if floatNum.is_integer() == True:
            return str(int(floatNum))
        else:
            return floatNum

class calculator:
    def __init__(self):
        #button name: [x, y, bg, fg, command]
        self.buttonsData = {
            "7": [0, 10, None, None, lambda: self.handleStandardB("7")],
            "8": [80, 10, None, None, lambda: self.handleStandardB("8")],
            "9": [160, 10, None, None, lambda: self.handleStandardB("9")],
            "DEL": [240, 10, "#0000ff", "#ffffff", lambda: self.handleDelB()],
            "AC": [320, 10, "#0000ff", "#ffffff", lambda: self.handleClearB()],
            "4": [0, 75, None, None, lambda: self.handleStandardB("4")],
            "5": [80, 75, None, None, lambda: self.handleStandardB("5")],
            "6": [160, 75, None, None, lambda: self.handleStandardB("6")],
            "x": [240, 75, None, None, lambda: self.handleStandardB("x")],
            "÷": [320, 75, None, None, lambda: self.handleStandardB("÷")],
            "1": [0, 140, None, None, lambda: self.handleStandardB("1")],
            "2": [80, 140, None, None, lambda: self.handleStandardB("2")],
            "3": [160, 140, None, None, lambda: self.handleStandardB("3")],
            "+": [240, 140, None, None, lambda: self.handleStandardB("+")],
            "-": [320, 140, None, None, lambda: self.handleStandardB("-")],
            ".": [0, 205, None, None, lambda: self.handleStandardB(".")],
            "0": [80, 205, None, None, lambda: self.handleStandardB("0")],
            "←": [160, 205, None, None, lambda: self.handleMovementB(-1)],
            "→": [240, 205, None, None, lambda: self.handleMovementB(1)],
            "=": [320, 205, None, None, lambda: self.handleEnterB()],
        }

    def handleStandardB(self, number: str): #number
        self.clearDisplayOutput()
        self.displayInput.focus_set()
        self.displayInput.insert(INSERT, number)

    def handleEnterB(self): #Enter
        self.clearDisplayOutput()

        equation = self.displayInput.get()
        calcParsers = calculationParsers()
        calcOutput = calcParsers.start(equation)

        self.displayOutput["state"] = NORMAL
        self.displayOutput.insert(0, calcOutput)
        self.displayOutput["state"] = DISABLED

    def handleClearB(self): #Clear
        self.clearDisplayOutput()
        self.displayInput.focus_set()
        self.displayInput.delete(0, END)

    def handleDelB(self): #delete
        self.clearDisplayOutput()
        self.displayInput.focus_set()
        displayInput_text = self.displayInput.get()[ :-1]
        self.displayInput.delete(0, END)
        self.displayInput.insert(INSERT, displayInput_text)

    def handleMovementB(self, direction: int): #pointer movement
        self.displayInput.focus_set()
        position = self.displayInput.index(INSERT)
        if direction == 1:
            equationLen = len(self.displayInput.get())
            if position + 1 <= equationLen:
                position += 1
        else:
            if position - 1 >= 0:
                position -= 1
        self.displayInput.icursor(position)

    def clearDisplayOutput(self):
        self.displayInput.focus_set()
        self.displayOutput["state"] = NORMAL
        self.displayOutput.delete(0, END)
        self.displayOutput["state"] = DISABLED

    def start(self):
        self.window = Tk()
        self.window.geometry("400x395")
        self.defaultbg = self.window.cget('bg')

        self.displayFrame = Frame(self.window, highlightthickness = 2, highlightbackground = "#000000")
        self.displayFrame.place(x = 2, y = 2, width = 396, height = 120)

        self.displayInput = Entry(
            self.displayFrame, font = ("Helevetica", 25), 
            relief = FLAT, bg = self.defaultbg, highlightthickness = 0
        )
        self.displayInput.place(x = 0, y = 0, width = 392, height = 46)
        self.displayInput.focus_set()

        self.displayOutput = Entry(
            self.displayFrame, font = ("Helevetica", 25), 
            justify = RIGHT, relief = FLAT, disabledforeground = "#000000"
        )
        self.displayOutput.place(x = 0, y = 70, width = 392, height = 45)
        self.displayOutput["state"] = DISABLED

        self.buttonFrame = Frame(self.window)
        self.buttonFrame.place(x = 0, y = 125, width = 400, height = 270)

        self.buttons = [
            Button(
                self.buttonFrame, text = item, font = ("Helevetica", 20), 
                bg = self.buttonsData[item][2], fg = self.buttonsData[item][3], 
                command = self.buttonsData[item][4]
            ).place(x = self.buttonsData[item][0], y = self.buttonsData[item][1], width = 80, height = 60) 
            for item in self.buttonsData
        ]

        self.window.mainloop()

calc = calculator()
calc.start()
