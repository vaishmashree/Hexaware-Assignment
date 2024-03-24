import pyodbc
from dao.serviceprovider import Customer_dao, Product_dao, Order_dao, Orderdetails_dao, Inventory_dao
from entity.customers import customers
from entity.orders import orders
from entity.products import products
from exception.AuthenticationException import AuthenticationException
from exception.AuthorizationException import AuthorizationException
from exception.ConcurrencyException import ConcurrencyException
from exception.DatabaseOfflineException import DatabaseOfflineException
from exception.FileIOException import FileIOException
from exception.IncompleteOrderException import IncompleteOrderException
from exception.InsufficientStockException import InsufficientStockException
from exception.InvalidDataException import InvalidDataException
from exception.PaymentFailedException import PaymentFailedException
from datetime import datetime
from decimal import Decimal


class Customer_daoImpl(Customer_dao):
    def __init__(self, connection):
        self.connection = connection

    def get_customer_by_id(self, customer_id):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT * FROM Customers WHERE CustomerID = ?"
            cursor.execute(sql, (customer_id,))
            customer = cursor.fetchone()
            cursor.close()
            return customer
        except pyodbc.Error as e:
            print(f"Error fetching customer: {e}")
            raise DatabaseOfflineException("Error fetching customer")

    def check_duplicate_email(self, email):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT COUNT(*) FROM Customers WHERE Email = ?"
            cursor.execute(sql, (email,))
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except pyodbc.Error as e:
            print(f"Error checking for duplicate email: {e}")
            raise InvalidDataException("Error checking for duplicate email")

    def add_customer(self, customer):
        try:
            if self.check_duplicate_email(customer.email):
                raise ValueError("Error: Email address already exists.")
            cursor = self.connection.cursor()
            sql = ("INSERT INTO Customers (CustomerID, FirstName, LastName, Email, Phone, Address) "
                   "VALUES (?, ?, ?, ?, ?, ?)")
            val = (customer.customerid, customer.firstname, customer.lastname, customer.email, customer.phone,
                   customer.address)
            cursor.execute(sql, val)
            self.connection.commit()
            cursor.close()
            return True
        except pyodbc.Error as e:
            print(f"Error creating customer: {e}")
            raise InvalidDataException("Error creating customer")

    def update_customer_info(self, customer_id, email=None, phone=None, address=None):
        try:
            cursor = self.connection.cursor()
            sql = "UPDATE Customers SET"
            val = []

            if email is not None:
                sql += " Email=?,"
                val.append(email)

            if phone is not None:
                sql += " Phone=?,"
                val.append(phone)

            if address is not None:
                sql += " Address=?,"
                val.append(address)

            # Remove the trailing comma from the SQL query
            if len(val) > 0:
                sql = sql.rstrip(',')
                sql += " WHERE CustomerID=?"
                val.append(customer_id)

                cursor.execute(sql, val)
                self.connection.commit()
                cursor.close()
                return True
            else:
                print("No parameters provided for update")
                return False
        except pyodbc.Error as e:
            print(f"Error updating customer: {e}")
            raise DatabaseOfflineException("Error updating customer")

    def delete_customer(self, customer_id):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM Customers WHERE CustomerID = ?"
            cursor.execute(sql, (customer_id,))
            self.connection.commit()
            cursor.close()
            return True
        except pyodbc.Error as e:
            print(f"Error deleting customer: {e}")
            raise DatabaseOfflineException("Error deleting customer")

    def get_all_customers(self):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT * FROM Customers"
            cursor.execute(sql)
            customers = cursor.fetchall()
            cursor.close()
            return customers
        except pyodbc.Error as e:
            print(f"Error fetching customers: {e}")
            raise DatabaseOfflineException("Error fetching customers")

    def calculate_total_orders(self, customer_id):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT COUNT(*) FROM Orders WHERE CustomerID = ?"
            cursor.execute(sql, (customer_id,))
            total_orders = cursor.fetchone()[0]
            cursor.close()
            return total_orders
        except pyodbc.Error as e:
            print(f"Error calculating total orders: {e}")
            raise InvalidDataException("Error calculating total orders")


class Product_daoImpl(Product_dao):
    def __init__(self, connection):
        self.connection = connection

    def get_product_by_id(self, product_id):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT * FROM Products WHERE ProductID = ?"
            cursor.execute(sql, (product_id,))
            product = cursor.fetchone()
            cursor.close()
            return product
        except pyodbc.Error as e:
            print(f"Error fetching product: {e}")
            raise DatabaseOfflineException("Error fetching product")

    def add_products(self, product):
        try:
            cursor = self.connection.cursor()

            # Insert product into Products table
            sql_insert_product = "INSERT INTO Products (ProductID, ProductName, Description, Price) VALUES (?, ?, ?, ?)"
            product_data = (product.productid, product.productname, product.description, product.price)
            cursor.execute(sql_insert_product, product_data)
            self.connection.commit()

            # Insert product into Inventory table
            sql_insert_inventory = "INSERT INTO Inventory (ProductID, QuantityInStock, LastStockUpdate) VALUES (?, ?, GETDATE())"
            inventory_data = (product.productid, 0)  # Assuming initial stock quantity is 0
            cursor.execute(sql_insert_inventory, inventory_data)
            self.connection.commit()

            return True
        except pyodbc.Error as e:
            print(f"Error adding product: {e}")
            raise InvalidDataException("Error adding product")

    def is_product_in_stock(self, product_id):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT QuantityInStock FROM Inventory WHERE ProductID = ?"
            cursor.execute(sql, (product_id,))
            total_stock = cursor.fetchone()
            cursor.close()
            if total_stock and total_stock[0] > 0:
                return True
            else:
                raise InsufficientStockException("Product is out of stock or not available")
        except pyodbc.Error as e:
            print(f"Error checking product stock: {e}")
            raise DatabaseOfflineException("Error checking product stock")

    def update_product_info(self, product_id, new_price=None):
        try:
            cursor = self.connection.cursor()
            sql = "UPDATE Products SET"
            val = []

            if new_price is not None:
                sql += " Price=?,"
                val.append(new_price)

            if len(val) > 0:
                sql = sql.rstrip(',')
                sql += " WHERE ProductID=?"
                val.append(product_id)

                cursor.execute(sql, val)
                self.connection.commit()
                cursor.close()
                return True
            else:
                print("No parameters provided for update")
                return False
        except pyodbc.Error as e:
            print(f"Error updating product: {e}")
            raise DatabaseOfflineException("Error updating product")

    def delete_products(self, product_id):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM Products WHERE ProductID = ?"
            cursor.execute(sql, (product_id,))
            self.connection.commit()
            cursor.close()
            return True
        except pyodbc.Error as e:
            print(f"Error deleting product: {e}")
            raise DatabaseOfflineException("Error deleting product")

    def get_all_products(self):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT * FROM Products"
            cursor.execute(sql)
            products = cursor.fetchall()
            cursor.close()
            return products
        except pyodbc.Error as e:
            print(f"Error fetching products: {e}")
            raise DatabaseOfflineException("Error fetching products")


class Order_daoImpl(Order_dao):
    def __init__(self, connection):
        self.connection = connection

    def create_orders(self, order, order_details):
        try:
            cursor = self.connection.cursor()
            total_amount = 0
            for order_detail in order_details:
                if order_detail.product is None:
                    raise IncompleteOrderException("Product reference missing in order details")
                sql_get_price = "SELECT Price FROM Products WHERE ProductID = ?"
                cursor.execute(sql_get_price, (order_detail.product,))
                price_row = cursor.fetchone()
                if price_row is not None:
                    price = price_row[0]
                    total_amount += order_detail.quantity * price
                else:
                    raise InvalidDataException(f"Product with ID {order_detail.product} not found in the database")

                if not Product_daoImpl(self.connection).is_product_in_stock(order_detail.product):
                    raise InsufficientStockException("Insufficient stock for one or more products")

            sql_insert_order = "INSERT INTO Orders (orderid, CustomerID, OrderDate, TotalAmount, Status) VALUES (?, ?, ?, ?, ?)"
            order_data = (order.orderid, order.customer, order.orderdate, total_amount, order.status)
            cursor.execute(sql_insert_order, order_data)
            self.connection.commit()

            sql_insert_order_detail = "INSERT INTO OrderDetails (OrderID, ProductID, Quantity) VALUES (?, ?, ?)"
            for order_detail in order_details:
                cursor.execute(sql_insert_order_detail, (order.orderid, order_detail.product, order_detail.quantity))
                Inventory_daoImpl(self.connection).updateStock(order_detail.product, order_detail.quantity)

            self.connection.commit()
            return True
        except pyodbc.Error as e:
            print(f"Error creating order: {e}")
            raise InvalidDataException("Error creating order")

    def display_orders(self):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT * FROM Orders"
            cursor.execute(sql)
            orders = cursor.fetchall()
            cursor.close()
            return orders
        except pyodbc.Error as e:
            print(f"Error fetching orders: {e}")
            raise DatabaseOfflineException("Error fetching orders")
    
    def get_order_details(self, orderId):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT * FROM Orders WHERE OrderID = ?"
            cursor.execute(sql, (orderId,))
            results = cursor.fetchall()
            orders_list = []
            for row in results:
                order = orders(row[0], row[1], row[2], row[3], row[4])  # Assuming orderid, customerid, orderdate, totalamount, and status are in respective positions in the row
                orders_list.append(order)
            cursor.close()
            return orders_list
        except pyodbc.Error as e:
            print(f"Error fetching order details: {e}")
            raise DatabaseOfflineException("Error fetching order details")
    def UpdateOrderStatus(self,orderid,new_status):
        try:
            cursor=self.connection.cursor()
            sql="update orders set status=? where orderid=?"
            cursor.execute(sql,(new_status,orderid,))
            self.connection.commit()
            cursor.close()
            return "Updated Successfully"
        except pyodbc.Error as err:
            print(f"Error updating order status : {err}")
            raise DatabaseOfflineException("Error updating order status")
    def calculate_total_amount(self):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT SUM(TotalAmount) FROM Orders"
            cursor.execute(sql)
            total_amount = cursor.fetchone()[0]
            cursor.close()
            return total_amount
        except pyodbc.Error as e:
            print(f"Error calculating total amount: {e}")
            raise DatabaseOfflineException("Error calculating total amount")
    def CancelOrder(self, order_id):
        try:
            cursor = self.connection.cursor()
            sql_check_order = "SELECT * FROM Orders WHERE OrderID = ?"
            cursor.execute(sql_check_order, (order_id,))
            order = cursor.fetchone()
            if not order:
                print("Order not found.")
                return False
            sql_delete_order = "DELETE FROM Orders WHERE OrderID = ?"
            cursor.execute(sql_delete_order, (order_id,))
            self.connection.commit()
            return True
        except pyodbc.Error as e:
            self.connection.rollback()
            print(f"Error deleting order: {e}")
            return False


class Inventory_daoImpl:
    def __init__(self, connection):
        self.connection = connection

    def updateStock(self, productId, quantity):
        try:
            cursor = self.connection.cursor()
            sql = "UPDATE Inventory SET QuantityInStock = QuantityInStock + ? WHERE ProductID = ?"
            cursor.execute(sql, (quantity, productId))
            self.connection.commit()
            cursor.close()
            return True
        except pyodbc.Error as e:
            print(f"Error updating stock: {e}")
            raise DatabaseOfflineException("Error updating stock")

    def getStock(self, productId):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT QuantityInStock FROM Inventory WHERE ProductID = ?"
            cursor.execute(sql, (productId,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return result[0]
            else:
                raise InvalidDataException("Product not found")
        except pyodbc.Error as e:
            print(f"Error fetching stock: {e}")
            raise DatabaseOfflineException("Error fetching stock")

    def get_inventory_info(self, inventory_id):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT * FROM Inventory WHERE InventoryID = ?"
            cursor.execute(sql, (inventory_id,))
            inventory_info = cursor.fetchone()
            cursor.close()
            return inventory_info
        except pyodbc.Error as e:
            print(f"Error fetching inventory info: {e}")
            raise DatabaseOfflineException("Error fetching inventory info")

    def list_all_products(self):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT * FROM Inventory"
            cursor.execute(sql)
            products = cursor.fetchall()
            cursor.close()
            if products:
                print("Listing all products in inventory:")
                for product in products:
                    print(product)
            else:
                print("No products found in inventory.")
        except pyodbc.Error as e:
            print(f"Error listing all products: {e}")
            raise DatabaseOfflineException("Error listing all products")

    def get_product(self, inventory_id):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT * FROM Inventory WHERE InventoryID = ?"
            cursor.execute(sql, (inventory_id,))
            product = cursor.fetchone()
            cursor.close()
            if product:
                print("Product details:")
                print(product)
            else:
                print("Product not found.")
        except pyodbc.Error as e:
            print(f"Error getting product details: {e}")
            raise DatabaseOfflineException("Error getting product details")

    def add_to_inventory(self, inventory_id, quantity):
        try:
            cursor = self.connection.cursor()
            sql = "UPDATE Inventory SET QuantityInStock = QuantityInStock + ? WHERE InventoryID = ?"
            cursor.execute(sql, (quantity, inventory_id))
            self.connection.commit()
            cursor.close()
            print("Product quantity added to inventory successfully.")
        except pyodbc.Error as e:
            print(f"Error adding product to inventory: {e}")
            raise DatabaseOfflineException("Error adding product to inventory")

    def remove_from_inventory(self, inventory_id, quantity):
        try:
            cursor = self.connection.cursor()
            sql = "UPDATE Inventory SET QuantityInStock = QuantityInStock - ? WHERE InventoryID = ?"
            cursor.execute(sql, (quantity, inventory_id))
            self.connection.commit()
            cursor.close()
            print("Product quantity removed from inventory successfully.")
        except pyodbc.Error as e:
            print(f"Error removing product from inventory: {e}")
            raise DatabaseOfflineException("Error removing product from inventory")

    def update_stock_quantity(self, inventory_id, new_quantity):
        try:
            cursor = self.connection.cursor()
            sql = "UPDATE Inventory SET QuantityInStock = ? WHERE InventoryID = ?"
            cursor.execute(sql, (new_quantity, inventory_id))
            self.connection.commit()
            cursor.close()
            print("Stock quantity updated successfully.")
        except pyodbc.Error as e:
            print(f"Error updating stock quantity: {e}")
            raise DatabaseOfflineException("Error updating stock quantity")

    def is_product_available(self, inventory_id, quantity_to_check):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT QuantityInStock FROM Inventory WHERE InventoryID = ?"
            cursor.execute(sql, (inventory_id,))
            result = cursor.fetchone()
            cursor.close()
            if result and result[0] >= quantity_to_check:
                print("Product is available in sufficient quantity.")
            else:
                print("Product is not available in sufficient quantity.")
        except pyodbc.Error as e:
            print(f"Error checking product availability: {e}")
            raise DatabaseOfflineException("Error checking product availability")

    def get_inventory_value(self, inventory_id):
        try:
            cursor = self.connection.cursor()
            sql = """
            SELECT SUM(i.QuantityInStock * p.Price)
            FROM Inventory i
            INNER JOIN Products p ON i.ProductID = p.ProductID
            WHERE i.InventoryID = ?
            """
            cursor.execute(sql, (inventory_id,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return result[0]
            else:
                raise InvalidDataException("Inventory ID not found")
        except pyodbc.Error as e:
            print(f"Error calculating inventory value: {e}")
            raise DatabaseOfflineException("Error calculating inventory value")

    def list_low_stock_products(self, threshold):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT * FROM Inventory WHERE QuantityInStock < ?"
            cursor.execute(sql, (threshold,))
            products = cursor.fetchall()
            cursor.close()
            if products:
                print("Listing low stock products:")
                for product in products:
                    print(product)
            else:
                print("No low stock products found.")
        except pyodbc.Error as e:
            print(f"Error listing low stock products: {e}")
            raise DatabaseOfflineException("Error listing low stock products")

    def list_out_of_stock_products(self):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT * FROM Inventory WHERE QuantityInStock <= 0"
            cursor.execute(sql)
            products = cursor.fetchall()
            cursor.close()
            if products:
                print("Listing out-of-stock products:")
                for product in products:
                    print(product)
            else:
                print("No out-of-stock products found.")
        except pyodbc.Error as e:
            print(f"Error listing out-of-stock products: {e}")
            raise DatabaseOfflineException("Error listing out-of-stock products")





class Orderdetails_daoImpl(Orderdetails_dao):
    def __init__(self, connection):
        self.connection = connection

    def deleteOrderDetails(self, orderDetailId):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM OrderDetails WHERE OrderDetailID = ?"
            cursor.execute(sql, (orderDetailId,))
            self.connection.commit()
            cursor.close()
            return True
        except pyodbc.Error as e:
            print(f"Error deleting order details: {e}")
            raise DatabaseOfflineException("Error deleting order details")

    def GetOrderDetailInfo(self, orderId):  # Corrected method name
        try:
            cursor = self.connection.cursor()
            sql = "SELECT * FROM OrderDetails WHERE OrderdetailID = ?"
            cursor.execute(sql, (orderId,))
            results = cursor.fetchall()
            cursor.close()
            return results
        except pyodbc.Error as e:
            print(f"Error fetching order details: {e}")
            raise DatabaseOfflineException("Error fetching order details")
        
    def UpdateQuantity(self,orderdetailid,new_quantity):
        try:
            cursor=self.connection.cursor()
            sql="update orderdetails set quantity=? where orderdetailid=?"
            cursor.execute(sql,(new_quantity,orderdetailid))
            self.connection.commit()
            cursor.close()
            return "Quantity updated successfully"
        except pyodbc.Error as err:
            print(f"Error updating quantity : {err}")
            raise DatabaseOfflineException("Error updating stock")
        

    def GetAllOrderDetail(self):
        try:
            cursor = self.connection.cursor()
            sql = "SELECT * FROM OrderDetails"
            cursor.execute(sql)
            order_details = cursor.fetchall()
            cursor.close()
            return order_details
        except pyodbc.Error as e:
            print(f"Error fetching order details: {e}")
            raise DatabaseOfflineException("Error fetching order details")
    def CalculateSubtotal(self, order_detail_id):
        try:
            cursor = self.connection.cursor()
            sql = """
                SELECT od.Quantity, p.Price
                FROM OrderDetails od
                INNER JOIN Products p ON od.ProductID = p.ProductID
                WHERE od.OrderDetailID = ?
            """
            cursor.execute(sql, (order_detail_id,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                quantity, price = result
                subtotal = quantity * price
                return subtotal
            else:
                raise InvalidDataException("Order detail not found")
        except pyodbc.Error as e:
            print(f"Error calculating subtotal: {e}")
            raise DatabaseOfflineException("Error calculating subtotal")
        
    def AddDiscount(self, order_detail_id, discount_percentage):
        try:
            cursor = self.connection.cursor()

            # Query to join OrderDetails and Products tables
            sql_get_price = """
                SELECT OD.OrderDetailID, OD.OrderID, OD.ProductID, P.Price
                FROM OrderDetails OD
                INNER JOIN Products P ON OD.ProductID = P.ProductID
                WHERE OD.OrderDetailID = ?
            """
            cursor.execute(sql_get_price, (order_detail_id,))
            order_detail_info = cursor.fetchone()

            if not order_detail_info:
                print("Order detail not found")
                return False

            # Extract the price from the result
            product_price = float(order_detail_info[3])

            # Calculate discounted price
            discounted_price = product_price * (1 - discount_percentage / 100)

            # Pri
            print(f"Original Price: ${product_price}")
            print(f"Discounted Percentage: {discount_percentage}%")
            print(f"Discounted Price: ${discounted_price:.2f}")

            cursor.close()
            return True
        except pyodbc.Error as e:
            print(f"Error calculating discounted amount: {e}")
            raise DatabaseOfflineException("Error calculating discounted amount")


class DatabaseManager:
    def __init__(self, connection):
        self.connection = connection

    def close_connection(self):
        try:
            self.connection.close()
            print("Database connection closed")
        except pyodbc.Error as e:
            print(f"Error closing database connection: {e}")





