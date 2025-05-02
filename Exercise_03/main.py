# Import neccessary modules
from easy_shopping import calculator

# Main function
def main():
    calc = calculator.calculator()
    print(calc.add(7,5))
    print(calc.substract(34,21))
    print(calc.multiply(54,2))
    print(calc.divide(144,2))
    print(calc.divide(45,0))
    print(calc.add(7,"a"))

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()