"""Products Class:
Attributes:
• ProductID (int)
• ProductName (string)
• Description (string)
• Price (decimal)
Methods:
• GetProductDetails(): Retrieves and displays detailed information about the product.
• UpdateProductInfo(): Allows updates to product details (e.g., price, description).
• IsProductInStock(): Checks if the product is currently in stock."""

class products:
    def __init__(self,productid,productname,description,price):
        self.__productid=productid
        self.__productname=productname
        self.__description=description
        self.__price=price
    
    @property
    def productid(self):
        return self.__productid

    @productid.setter
    def productid(self, productid):
        self.__productid = productid

    @property
    def productname(self):
        return self.__productname

    @productname.setter
    def productname(self, productname):
        self.__productname = productname

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, desc):
        self.__description = desc

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value


    def GetProductDetails(self):
        return (f"Product ID : {self.productid}\n"
                f"Product Name : {self.productname}\n"
                f"Description : {self.description}\n"
                f"Price : ${self.price:.2f}")
    
    def UpdateProductInfo(self,price,description):
        if price:
            self.price=price
        if description:
            self.description=description
    
    def IsProductInStock(self):
        pass
    
