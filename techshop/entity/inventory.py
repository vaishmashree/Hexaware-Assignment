"""Inventory class:
Attributes:
• InventoryID(int)
• Product (Composition): The product associated with the inventory item.
• QuantityInStock: The quantity of the product currently in stock.
• LastStockUpdate
Methods:
• GetProduct(): A method to retrieve the product associated with this inventory item.
• GetQuantityInStock(): A method to get the current quantity of the product in stock.
• AddToInventory(int quantity): A method to add a specified quantity of the product to the inventory.
• RemoveFromInventory(int quantity): A method to remove a specified quantity of the product from the inventory.
• UpdateStockQuantity(int newQuantity): A method to update the stock quantity to a new value.
• IsProductAvailable(int quantityToCheck): A method to check if a specified quantity of the product is available in the inventory.
• GetInventoryValue(): A method to calculate the total value of the products in the inventory based on their prices and quantities.
• ListLowStockProducts(int threshold): A method to list products with quantities below a specified threshold, indicating low stock.
• ListOutOfStockProducts(): A method to list products that are out of stock.
• ListAllProducts(): A method to list all products in the inventory, along with their quantities."""

from products import products

class inventory:
    def __init__(self,inventoryid,product,quantityinstock,laststockupdate):
        self.__inventoryid=inventoryid
        self.__product=product
        self.__quantityinstock=quantityinstock
        self.__laststockupdate=laststockupdate

    @property
    def inventoryid(self):
        return self.__inventoryid

    @inventoryid.setter
    def inventoryid(self, inventoryid):
        self.__inventoryid = inventoryid

    @property
    def product(self):
        return self.__product

    @product.setter
    def product(self, product):
        self.__product = product

    @property
    def quantityinstock(self):
        return self.__quantityinstock

    @quantityinstock.setter
    def quantityinstock(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity in stock cannot be negative")
        self.__quantityinstock = quantity

    @property
    def laststockupdate(self):
        return self.__laststockupdate

    @laststockupdate.setter
    def laststockupdate(self, value):
        self.__laststockupdate = value

    def GetProduct(self):
        return self.product
    
    def GetQuantityInStock(self):
        return self.quantityinstock
    
    def AddToInventory(self,quantity):
        self.quantityinstock += quantity

    def RemoveFromInventory(self,quantity):
        self.quantityinstock-=quantity
    
    def UpdateStockQuantity(self,quantiy):
        self.quantityinstock=quantiy

    def IsProductAvailable(self):
        if self.quantityinstock > 0:
            return True
        else:
            return False
    
    def GetInventoryValue(self):
        return self.product.price * self.quantityinstock
    
    def ListLowStockProducts(self,threshold):
        if self.quantityinstock<threshold:
            return f"{self.product.productname}:{self.quantityinstock}"
        
    def ListOutOfStockProducts(self):
        if self.quantityinstock==0:
            return self.product.productname
        
    def ListAllProducts(self):
        for i in products:
            return products.productname