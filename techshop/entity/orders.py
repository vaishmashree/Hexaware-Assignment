"""Orders Class:
Attributes:
• OrderID (int)
• Customer (Customer) - Use composition to reference the Customer who placed the order.
• OrderDate (DateTime)
• TotalAmount (decimal)
Methods:
• CalculateTotalAmount() - Calculate the total amount of the order.
• GetOrderDetails(): Retrieves and displays the details of the order (e.g., product list and quantities).
• UpdateOrderStatus(): Allows updating the status of the order (e.g., processing, shipped).
• CancelOrder(): Cancels the order and adjusts stock levels for products."""


class orders:
    def __init__(self,orderid,customer,orderdate,totalamount,status):
        self.__orderid=orderid
        self.__customer=customer
        self.__orderdate=orderdate
        self.__totalamount=totalamount
        self.__status=status

    @property
    def orderid(self):
        return self.__orderid

    @orderid.setter
    def orderid(self, orderid):
        self.__orderid = orderid

    @property
    def customer(self):
        return self.__customer

    @customer.setter
    def customer(self, customer):
        self.__customer = customer

    @property
    def orderdate(self):
        return self.__orderdate

    @orderdate.setter
    def orderdate(self, ordate):
        self.__orderdate = ordate

    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self,status):
        self.__status=status

    @property
    def totalamount(self):
        return self.__totalamount

    @totalamount.setter
    def totalamount(self, amount):
        if amount < 0:
            raise ValueError("Total amount cannot be negative")
        self.__totalamount = amount

    def CalculateTotalAmount(self):
        return self.totalamount
    
    def GetOrderDetails(self):
        return (f"Order ID : {self.orderid}\n"
                f"Customer : {self.customer}\n"
                f"Order Date : {self.orderdate}\n"
                f"Total Amount : {self.totalamount}\n")
    
    def UpdateOrderStatus(self,status):
        pass

    def CancelOrder(self):
        self.cancel=True
        