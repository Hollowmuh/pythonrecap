class AdvancedCalculator:
    def __init__(self):
        self.result = None
    
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b  # Fixed subtraction

    def multiply(self, a, b):
        return a * b  # Fixed multiplication

    def divide(self, a, b):
        if b == 0:
            return "Error: Division by zero is not allowed."
        else:
            return a / b

    def power(self, a, b):
        return a ** b

    def calculate(self, operation, x, y):
        # Mapping operation names to methods for clarity
        operations = {
            "add": self.add,
            "subtract": self.subtract,
            "multiply": self.multiply,
            "divide": self.divide,
            "power": self.power
        }
        func = operations.get(operation)
        if func:
            return func(x, y)
        else:
            return "Invalid operation."


def main():
    calc = AdvancedCalculator()
    while True:
        try:
            user_input = input("Enter a number or operator (+, -, *, /, ^) or 'q' to exit: ").strip()
            if user_input.lower() == "q":
                print("Exiting the calculator.")
                break
            # If input is an operator
            if user_input in ["+", "-", "*", "/", "^"]:
                if calc.result is None:
                    print("No previous calculation. Please enter a number first.")
                    continue
                num2_input = input("Enter second number: ").strip()
                try:
                    num2 = float(num2_input)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue
                operation_map = {
                    "+": 'add',
                    "-": 'subtract',
                    "*": 'multiply',
                    "/": 'divide',   
                    "^": 'power'
                }
                calc.result = calc.calculate(operation_map[user_input], calc.result, num2)
                print(f"Result: {calc.result}")
            else:
                # Try converting to a float to handle numbers (including negatives)
                try:
                    calc.result = float(user_input)
                    print(f"Current number: {calc.result}")
                except ValueError:
                    print("Invalid input. Please enter a number or a valid operator.")
        except Exception as e:
            print(f"An error occurred: {e}")
            calc.result = None

if __name__ == "__main__":
    main()
