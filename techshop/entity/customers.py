"""Customers Class:
Attributes:
• CustomerID (int)
• FirstName (string)
• LastName (string)
• Email (string)
• Phone (string)
• Address (string)
Methods:
• CalculateTotalOrders(): Calculates the total number of orders placed by this customer.
• GetCustomerDetails(): Retrieves and displays detailed information about the customer.
• UpdateCustomerInfo(): Allows the customer to update their information (e.g., email, phone, or address)."""


class customers:
    def __init__(self,customerid,firstname,lastname,email,phone,address):
        self.__customerid=customerid
        self.__firstname=firstname
        self.__lastname=lastname
        self.__email=email
        self.__phone=phone
        self.__address=address
    
    @property
    def customerid(self):
        return self.__customerid

    @property
    def firstname(self):
        return self.__firstname

    @property
    def lastname(self):
        return self.__lastname

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value):
        self.__phone = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value

    def CalculateTotalOrder(self):
        return self.phone
    
    def GetCustomerDetails(self):
        return (f"CustomerID : {self.customerid}\n"
                f"FirstName : {self.firstname}\n"
                f"LastName : {self.lastname}\n" 
                f"Email : {self.email}\n"
                f"Phone : {self.phone}\n"
                f"Address : {self.address}\n")
    def UpdateCustomerInfo(self,email=None,phone=None,address=None):
        if email:
            self.email=email
        if phone:
            self.phone=phone
        if address:
            self.address=address
