# Import neccessary modules
from easy_shopping import calculator
from easy_shopping import shopping

# Main function
def main():
    calc = calculator.calculator()
    print("----- Test Cases for calculator -----")
    print(calc.add(7,5))
    print(calc.substract(34,21))
    print(calc.multiply(54,2))
    print(calc.divide(144,2))
    print(calc.divide(45,0))
    print(calc.add(7,"a"))

    cart = shopping.cart([])
    print("----- Test Cases for shopping cart -----")
    print(cart.addItem("Milk", 3))
    print(cart.addItem("Cheese", 1))
    print(cart.addItem("Rolls", 10))
    print(cart.addItem("Cheese", 3))
    print(cart.displayInventory())
    print(cart.removeItem("Cheese", 2))
    print(cart.removeItem("Rolls", 5))
    print(cart.removeItem("Cheese", 3))

# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()