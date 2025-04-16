import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel
from PySide6.QtGui import QDoubleValidator
import math

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prosty Kalkulator")
        self.resize(400, 400)

        # Pola tekstowe
        self.input1 = QLineEdit(self)
        self.input1.setGeometry(50, 20, 150, 30)
        self.input1.setPlaceholderText("Podaj liczbę")
        self.input1.setValidator(QDoubleValidator())  
        
        self.input2 = QLineEdit(self)
        self.input2.setGeometry(220, 20, 150, 30)
        self.input2.setPlaceholderText("Podaj liczbę")
        self.input2.setValidator(QDoubleValidator()) 

        # Wyświetlanie wyniku
        self.result_label = QLabel(self)
        self.result_label.setGeometry(50, 60, 320, 30)
        self.result_label.setText(" ")
        self.result_label.setStyleSheet("font-size: 20px; color: yellow;")

        # Tworzenie przycisków
        self.create_buttons()

    def create_buttons(self):
        button_size = 50
        spacing = 10
        start_x = 50
        start_y = 100

        number_grid = [
            [7, 8, 9],
            [4, 5, 6],
            [1, 2, 3],
            [None, 0, None]
        ]

        for row_index, row in enumerate(number_grid):
            for col_index, num in enumerate(row):
                if num is not None:
                    button = QPushButton(str(num), self)
                    button.setGeometry(start_x + col_index * (button_size + spacing), start_y + row_index * (button_size + spacing), button_size, button_size)
                    button.clicked.connect(lambda checked, n=num: self.append_number(n))

        # Operacje matematyczne
        operations = [
            ("+", 3, 0),  # Plus pod 1
            ("-", 3, 2),  # Minus pod 3
            ("/", 0, 3),  # Dzielenie u góry
            ("x", 1, 3),  # Mnożenie poniżej dzielenia
            ("√", 2, 3),  # Pierwiastkowanie poniżej mnożenia
            (".", 3, 3)   # Liczby dziesiętne poniżej dzielenia
        ]

        for symbol, row, col in operations:
            button = QPushButton(symbol, self)
            button.setGeometry(start_x + col * (button_size + spacing), start_y + row * (button_size + spacing), button_size, button_size)
            button.clicked.connect(lambda checked, op=symbol: self.perform_operation(op))

    def append_number(self, num):
        if self.input1.hasFocus():
            self.input1.setText(self.input1.text() + str(num))
        elif self.input2.hasFocus():
            self.input2.setText(self.input2.text() + str(num))

    def get_inputs(self):
        try:
            num1 = float(self.input1.text())
            num2 = float(self.input2.text())
            return num1, num2
        except ValueError:
            self.result_label.setText("Błędne dane!")
            return None, None

    def perform_operation(self, operation):
        num1, num2 = self.get_inputs()
        if num1 is None:
            return

        if operation == "+" and num2 is not None:
            self.result_label.setText(f"= {num1 + num2}")
        elif operation == "-" and num2 is not None:
            self.result_label.setText(f"= {num1 - num2}")
        elif operation == "x" and num2 is not None:
            self.result_label.setText(f"= {num1 * num2}")
        elif operation == "/" and num2 is not None:
            if num2 == 0:
                self.result_label.setText("Nie dziel przez zero!")
            else:
                self.result_label.setText(f"= {num1 / num2}")
        elif operation == "√":
            self.result_label.setText(f"= {math.sqrt(num1):.2f}")
        elif operation == ".":
            if self.input1.hasFocus():
                if "." not in self.input1.text():
                    self.input1.setText(self.input1.text() + ".")
            elif self.input2.hasFocus():
                if "." not in self.input2.text():
                    self.input2.setText(self.input2.text() + ".")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())
