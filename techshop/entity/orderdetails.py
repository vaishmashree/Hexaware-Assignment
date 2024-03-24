"""OrderDetails Class:
Attributes:
• OrderDetailID (int)
• Order (Order) - Use composition to reference the Order to which this detail belongs.
• Product (Product) - Use composition to reference the Product included in the order detail.
• Quantity (int)
Methods:
• CalculateSubtotal() - Calculate the subtotal for this order detail.
• GetOrderDetailInfo(): Retrieves and displays information about this order detail.
• UpdateQuantity(): Allows updating the quantity of the product in this order detail.
• AddDiscount(): Applies a discount to this order detail."""


class orderdetails:
    def __init__(self,orderdetailid,order,product,quantity):
        self.__orderdetailid=orderdetailid
        self.__order=order
        self.__product=product
        self.__quantity=quantity

    @property
    def orderdetailid(self):
        return self.__orderdetailid

    @orderdetailid.setter
    def order_detail_id(self, orderdetailid):
        self.__orderdetailid = orderdetailid

    @property
    def order(self):
        return self.__order

    @order.setter
    def order(self, order):
        self.__order = order
    
    @property
    def product(self):
        return self.__product
    
    @product.setter
    def product(self, product):
        self.__product = product
    
    @property
    def quantity(self):
        return self.__quantity
    
    @quantity.setter
    def quantity(self, quan):
        if quan <= 0:
            raise ValueError("Quantity must be a positive integer")
        self.__quantity = quan

    def CalculateSubtotal(self):
        pass
    def GetOrderDetailInfo(self):
        return (f"Orderdetail ID: {self.orderdetailid}\n"
                f"Order : {self.order}\n"
                f"Product : {self.product}\n"
                f"Quantity : {self.quantity}")
    def UpdateQuantity(self,quantity):
        if quantity: 
            self.quantity=quantity
    def AddDiscount(self):
        pass