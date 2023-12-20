import sys
import math
from PyQt5.QtWidgets import *

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_button = QGridLayout()
        layout_equation_solution = QFormLayout()

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        self.screen_output = QLineEdit("")

        ### layout_equation_solution 레이아웃에 수식, 답 위젯을 추가
        layout_equation_solution.addRow(self.screen_output)

        ### 사칙연상 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("/")
        button_mod= QPushButton("%")
        button_inversion = QPushButton("1/x")
        button_squar = QPushButton("x^2")
        button_root = QPushButton("x^(1/2)")

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))
        button_inversion.clicked.connect(self.button_inversion_clicked)
        button_mod.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))
        button_squar.clicked.connect(self.button_squar_clicked)
        button_root.clicked.connect(self.button_root_clicked)

        ### 사칙연산 버튼을 layout_operation 레이아웃에 추가
        layout_button.addWidget(button_plus, 4, 3)
        layout_button.addWidget(button_minus, 3, 3)
        layout_button.addWidget(button_product, 2, 3)
        layout_button.addWidget(button_division, 1, 3)
        layout_button.addWidget(button_inversion, 1, 0)
        layout_button.addWidget(button_squar, 1, 1)
        layout_button.addWidget(button_root, 1, 2)
        layout_button.addWidget(button_mod, 0, 0)

        ### =, clear, backspace 버튼 생성
        button_equal = QPushButton("=")
        button_clear = QPushButton("C")
        button_CE = QPushButton("CE")
        button_backspace = QPushButton("<-")
        button_extra = QPushButton("+/-")

        ### =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_CE.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### =, clear, backspace 버튼을 layout_clear_equal 레이아웃에 추가
        layout_button.addWidget(button_clear, 0, 2)
        layout_button.addWidget(button_CE, 0, 1)
        layout_button.addWidget(button_backspace, 0, 3)
        layout_button.addWidget(button_equal, 5, 3)
        layout_button.addWidget(button_extra, 5, 0)

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            col=(number-1)%3
            if (number > 0) and (number <= 3):
                layout_button.addWidget(number_button_dict[number], 4, col)
            elif (number > 3) and (number <= 6):
                layout_button.addWidget(number_button_dict[number], 3, col)
            elif (number > 6) and (number <= 9):
                layout_button.addWidget(number_button_dict[number], 2, col)
            elif number==0:
                layout_button.addWidget(number_button_dict[number], 5, 1)

        ### 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_button.addWidget(button_dot, 5, 2)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_button)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num):
        equation = self.screen_output.text()
        if equation == "0":
            self.screen_output.setText(str(num))
        elif num == 0:
            pass
        elif equation=="" and num==".":
            pass
        else:
            equation += str(num)
            self.screen_output.setText(equation)

    def button_operation_clicked(self, operation):
        equation = self.screen_output.text()
        if equation=="":
            pass
        else:
            equation += operation
            self.screen_output.setText(equation)

    def button_equal_clicked(self):
        equation = self.screen_output.text()
        op=""
        op_index=0

        for i in equation:
            if i == "+" or i == "-" or i == "*" or i == "/" or i == "%":
                op=i
                break
            op_index += 1

        num1=equation[0:op_index]
        num2=equation[op_index+1:]

        if op=="+":
            output=float(num1)+float(num2)
        elif op=="-":
            output=float(num1)-float(num2)
        elif op=="*":
            output=float(num1)*float(num2)
        elif op=="/":
            output=float(num1)/float(num2)
        elif op=="%":
            output=int(num1)%int(num2)

        self.screen_output.setText(str(output))

    def button_clear_clicked(self):
        self.screen_output.setText("0")

    def button_backspace_clicked(self):
        equation = self.screen_output.text()
        equation = equation[:-1]
        self.screen_output.setText(equation)

    def button_inversion_clicked(self):
        equation = self.screen_output.text()
        try:
           number = float(equation)
           number = 1 / number
           output = str(number)
           self.screen_output.setText(output)

        except:
             self.screen_output.setText("")

    def button_squar_clicked(self):
        equation = self.screen_output.text()
        try:
           number = float(equation)
           number = number*number
           output = str(number)
           self.screen_output.setText(output)

        except:
             self.screen_output.setText("")

    def button_root_clicked(self):
        equation = self.screen_output.text()
        try:
           number = float(equation)
           number = number**(1/2)
           output = str(number)
           self.screen_output.setText(output)

        except:
             self.screen_output.setText("")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())