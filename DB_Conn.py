import pyodbc
import pymssql
SERVER = 'DESKTOP-F0AQSOF\SQLEXPRESS'
DATABASE = 'CRUD'
USERNAME = 'sa'
PASSWORD = 'djl123'
class DB_Conn:
    def readdata():
        print('conn details of using pyodbc')
        connectionString = f'DRIVER={{SQL Server Native Client 11.0}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
        conn = pyodbc.connect(connectionString)
        print('Connected..')
        SQL_QUERY = """
        SELECT 
        * from books;
        """
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)

        records = cursor.fetchall()
        print(records)



    def readdata_pymssql():
        print('conn details of pymssql')
        connectionString = f'SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
        #conn =  pymssql.connect(connectionString,as_dict=True)
        print(pymssql)
        conn = pymssql.Connection(server='.\SQLEXPRESS',user='sa',password=PASSWORD,database=DATABASE, as_dict=True)
        print('Connected..')
        SQL_QUERY = """
        SELECT 
        * from books;
        """
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)

        records = cursor.fetchall()
        print(records)

     
DB_Conn.readdata()
DB_Conn.readdata_pymssql()






