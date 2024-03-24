from abc import ABC, abstractmethod


class Customer_dao(ABC):
    @abstractmethod
    def add_customer(self, customer):
        pass

    @abstractmethod
    def delete_customer(self, customer):
        pass

    @abstractmethod
    def get_all_customers(self):
        pass


class Product_dao(ABC):
    @abstractmethod
    def add_products(self, product):
        pass

    @abstractmethod
    def delete_products(self, product_id):
        pass

    @abstractmethod
    def get_all_products(self):
        pass


class Order_dao(ABC):
    @abstractmethod
    def create_orders(self, order, order_details):
        pass

    @abstractmethod
    def display_orders(self):
        pass


class Orderdetails_dao(ABC):
    @abstractmethod
    def GetAllOrderDetail(self):
        pass


class Inventory_dao(ABC):
    @abstractmethod
    def get_inventory_info(self, inventory_id):
        pass