# Definition of class shopping_cart
class cart:
    # Construct a shopping cart with a list
    def __init__(self,inventory):
        self.inventory = []
    
    # Adds a dictionary to the list with a name and a quantity. 
    # If the item already exists, only the quantity gets updated.
    def addItem(self,item,quantity):
        contains = False
        # iterate through list, check if item exists
        for i in self.inventory:
            if i["name"] == item:
                i["quantity"] = i["quantity"] + quantity
                contains = True
                break
        # If item does not exists, new item dict is created
        if not contains:
            self.inventory.append({"name":item, "quantity":quantity})
        # Returning result as printable string
        return f"{item} with quantity {quantity} has been added to the cart. {self.displayInventory()}"

    # Creates string with inventory and total quantity
    def displayInventory(self):
        invString = ""
        totalQuantity = 0
        # iterating through list
        for i in self.inventory:
            invString = invString + f'{i["quantity"]}x {i["name"]}, '
            totalQuantity += i["quantity"]
        # Returning result as printable string
        return f"The inventory contains: {invString} | Total quantity: {totalQuantity}"
    
    # Removes a specified quantity of an item.
    # If quantity is lower or equal to zero, the item dict is removed from the inventory.
    def removeItem(self, item, quantity):
        contains = False
        # iterate through list, updating quantity or removing item
        for i in self.inventory:
            if i["name"] == item:
                i["quantity"] = i["quantity"] - quantity
                contains = True
                if i["quantity"] <= 0:
                    self.inventory.remove(i)
                    break
        # Returning result as printable string
        if contains:
            return f"{quantity}x {item} has been removed from the cart. {self.displayInventory()}"
        else:
            return f"{item} could not be removed. Element not in cart."