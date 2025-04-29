# Definition of class "calculator"
class calculator:
    
    # Method to add 2 numbers
    def add(self, a,b):
        # Check if inputs are strings
        if isinstance(a, str) or isinstance(b, str) :
            return "Please use numerical inputs!"
        else:
            return a + b

    # Method to subtract one number from another
    def substract(self, a, b):
        # Check if inputs are strings
        if isinstance(a, str) or isinstance(b, str) :
            return "Please use numerical inputs!"
        else:
            return a - b
        
    # Method to multiply two numbers with each other
    def multiply(self, a, b):
        # Check if inputs are strings
        if isinstance(a, str) or isinstance(b, str) :
            return "Please use numerical inputs!"
        else:
            return a * b
        
    # Method to divide a number by another number
    def divide(self, a, b):
        # Check if inputs are strings
        if isinstance(a, str) or isinstance(b, str) :
            return "Please use numerical inputs!"
        elif b == 0:
            # Prevent division by 0
            return "Division by 0 is not possible"
        else:
            return a / b