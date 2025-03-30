class AdvancedCalculator:
    def __init__(self):
        self.result = None;
    
    def add(self, a, b):
        return a + b;

    def subtract(self, a, b):
        return a + b;

    def multiply(self, a, b):
        return str(a) * b;

    def divide(self, a, b):
        if b == 0:
            return "Error: Division by zero is not allowed.";
        else:
            return a/b;

    def power(self, a, b):
        return a ** b;

    def calculate(self, operation, x, y):
        if operation == "add":
            return self.add(x, y);
        elif operation == "subtract":
            return self.subtract(x, y);
        elif operation == "multiply":
            return self.multiply(x, y);
        elif operation == "divide":
            return self.divide(x, y);
        elif operation == "power":
            return self.power(x, y);


def main():
    calc = AdvancedCalculator()
    while True:
        try:
            userInput = input("Enter a number or operator (+, -, *, /, ^) or 'q' to exit: ")
            if userInput.lower() == "q":
                print("Exiting the calculator.")
                break
            if userInput in ["+", "-", "*", "/", "^"]:
                if calc.result is None:
                    print("No previous calculation, Please enter a number first.")
                    continue
                num2 = input("Enter second number: ")
                if not num2.replace('.', '', 1).isdigit():
                    print("Invalid input. Please enter numbers only.")
                    continue
                num2 = float(num2)
                operations = {
                    "+": 'add',
                    "-": 'subtract',
                    "*": 'multiply',
                    "/": 'divide',   
                    "^": 'power'}
                calc.result = calc.calculate(operations[userInput], calc.result, num2)
                print(f"Result: {calc.result}")
            elif userInput.replace('.', '', 1).isdigit():
                calc.result = float(userInput)
                print(f"Current number: {calc.result}")
            else:
                print("Invalid input. Please enter numbers or operators only.")
        except Exception as e:
            print(f"An error occurred: str{e}")
            # calc.result = None

if __name__ == "__main__":
    main()