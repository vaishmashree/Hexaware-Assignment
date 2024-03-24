# import mysql.connector
# from mysql.connector import Error

# class DBConnection:
#     con = None

#     @staticmethod
#     def getConnection():
#         if DBConnection.con is None:
#             try:
#                 DBConnection.con = mysql.connector.connect(
#                     host='localhost',
#                     user='root',
#                     password='rootpass',
#                     database='techshop'
#                 )
#                 if DBConnection.con.is_connected():
#                     print("DB Connected !!!")
#             except Error as err:
#                 print(f"Error connecting DB: {err}")

#         return DBConnection.con


import pyodbc

class DBConnection:
    con = None

    @staticmethod
    def getConnection():
        if DBConnection.con is None:
            try:
                DBConnection.con = pyodbc.connect(
                    'Driver={SQL Server};'
                    'Server=HP\SQLEXPRESS;'
                    'Database=techshops;'
                )
                print("DB Connected !!!")
            except pyodbc.Error as err:
                print(f"Error connecting DB: {err}")

        return DBConnection.con

