"""
Database Connector Module
Handles all MySQL database connections and operations
"""

import mysql.connector
from mysql.connector import pooling
from dataclasses import dataclass
import pandas as pd


@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    host: str = '127.0.0.1'
    port: int = 3306
    user: str = 'root'
    password: str = ''
    database: str = 'etf_backtester_db'
    pool_name: str = 'etf_pool'
    pool_size: int = 5


class DatabaseConnector:
    """
    Database Connector with Connection Pooling
    """

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection_pool = None
        self._create_connection_pool()

    def _create_connection_pool(self):
        """Create connection pool"""
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name=self.config.pool_name,
                pool_size=self.config.pool_size,
                host=self.config.host,
                port=self.config.port,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database
            )
            print(f"  ✓ Connection pool created (size: {self.config.pool_size})")
        except mysql.connector.Error as err:
            print(f"  ✗ Error creating connection pool: {err}")
            raise

    def get_connection(self):
        """Get connection from pool"""
        try:
            return self.connection_pool.get_connection()
        except mysql.connector.Error as err:
            print(f"Error getting connection: {err}")
            raise

    def test_connection(self):
        """Test database connection"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            conn.close()
            print("  ✓ Database connection successful")
            return True
        except mysql.connector.Error as err:
            print(f"  ✗ Connection test failed: {err}")
            return False

    def execute_query(self, query, params=None):
        """Execute query and return results as list of tuples"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Query execution error: {err}")
            raise
        finally:
            cursor.close()
            conn.close()

    def execute_query_dict(self, query, params=None):
        """Execute query and return results as list of dictionaries"""
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Query execution error: {err}")
            raise
        finally:
            cursor.close()
            conn.close()

    def execute_update(self, query, params=None):
        """Execute INSERT/UPDATE/DELETE query"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            conn.commit()
            affected_rows = cursor.rowcount
            return affected_rows
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Update execution error: {err}")
            raise
        finally:
            cursor.close()
            conn.close()

    def execute_many(self, query, data_list):
        """Execute batch INSERT/UPDATE"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.executemany(query, data_list)
            conn.commit()
            return cursor.rowcount
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Batch execution error: {err}")
            raise
        finally:
            cursor.close()
            conn.close()

    def get_table_count(self, table_name):
        """Get row count from table"""
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        result = self.execute_query(query)
        return result[0][0] if result else 0

    def close_pool(self):
        """Close all connections in pool"""
        print("  ✓ Database connection pool closed")
