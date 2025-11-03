
import pyodbc
import os
from typing import Optional, Any
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection:

    def __init__(self):

        self.server = os.getenv('DB_SERVER', 'localhost,1433')
        self.database = os.getenv('DB_DATABASE', 'SistemaBiblioteca')
        self.username = os.getenv('DB_USERNAME', 'sa')
        self.password = os.getenv('DB_PASSWORD', 'BibliotecaFort3!')
        self.driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
        self.connection: Optional[pyodbc.Connection] = None

    def connect(self) -> bool:

        try:
            connection_string = (
                f"DRIVER={{{self.driver}}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
                f"TrustServerCertificate=yes;"
            )

            self.connection = pyodbc.connect(connection_string)
            return True

        except pyodbc.Error as e:
            print(f"✗ Erro ao conectar ao banco: {e}")
            return False
        except Exception as e:
            print(f"✗ Erro inesperado: {e}")
            return False

    def disconnect(self) -> None:

        if self.connection:
            self.connection.close()
            self.connection = None
            print("✓ Desconectado do banco de dados")

    def execute_query(self, query: str, params: tuple = ()) -> Optional[list]:

        if not self.connection:
            if not self.connect():
                return None

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)

            columns = [column[0]
                       for column in cursor.description] if cursor.description else []

            rows = cursor.fetchall()

            result = []
            for row in rows:
                row_dict = {}
                for i, value in enumerate(row):
                    row_dict[columns[i]] = value
                result.append(row_dict)

            cursor.close()
            return result

        except pyodbc.Error as e:
            print(f"✗ Erro ao executar consulta: {e}")
            return None
        except Exception as e:
            print(f"✗ Erro inesperado: {e}")
            return None

    def execute_non_query(self, query: str, params: tuple = ()) -> bool:

        if not self.connection:
            if not self.connect():
                return False

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            cursor.close()
            return True

        except pyodbc.Error as e:
            print(f"✗ Erro ao executar operação: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        except Exception as e:
            print(f"✗ Erro inesperado: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    def execute_scalar(self, query: str, params: tuple = ()) -> Any:

        if not self.connection:
            if not self.connect():
                return None

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            cursor.close()

            return result[0] if result else None

        except pyodbc.Error as e:
            print(f"✗ Erro ao executar consulta escalar: {e}")
            return None
        except Exception as e:
            print(f"✗ Erro inesperado: {e}")
            return None

    def test_connection(self) -> bool:

        try:
            result = self.execute_scalar("SELECT 1")
            return result == 1
        except BaseException:
            return False

    def __enter__(self):

        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.disconnect()


_db_connection = None


def get_connection():

    global _db_connection

    if _db_connection is None:
        _db_connection = DatabaseConnection()

    if not _db_connection.connection or not _db_connection.test_connection():
        if not _db_connection.connect():
            raise Exception("Não foi possível conectar ao banco de dados")

    return _db_connection.connection


def close_connection():

    global _db_connection
    if _db_connection:
        _db_connection.disconnect()
        _db_connection = None
