"""
Database Connector Module for ETF Backtester
Handles all MySQL database connections and operations
"""

import mysql.connector
from mysql.connector import Error, pooling
import os
from typing import Optional, List, Dict, Any, Tuple
from contextlib import contextmanager
import json


class DatabaseConfig:
    """Database configuration handler"""

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize database configuration

        Args:
            config_file: Optional path to JSON config file
        """
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
        else:
            # Default configuration (can be overridden by environment variables)
            self.host = os.getenv('DB_HOST', 'localhost')
            self.port = int(os.getenv('DB_PORT', '3306'))
            self.database = os.getenv('DB_NAME', 'etf_backtester_db')
            self.user = os.getenv('DB_USER', 'root')
            self.password = os.getenv('DB_PASSWORD', 'password')
            self.pool_name = 'etf_pool'
            self.pool_size = 5

    def load_from_file(self, config_file: str):
        """Load configuration from JSON file"""
        with open(config_file, 'r') as f:
            config = json.load(f)
            self.host = config.get('host', 'localhost')
            self.port = config.get('port', 3306)
            self.database = config.get('database', 'etf_backtester_db')
            self.user = config.get('user', 'root')
            self.password = config.get('password', '')
            self.pool_name = config.get('pool_name', 'etf_pool')
            self.pool_size = config.get('pool_size', 5)

    def to_dict(self) -> dict:
        """Convert config to dictionary for mysql.connector"""
        return {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'user': self.user,
            'password': self.password
        }


class DatabaseConnector:
    """
    Main database connector class using connection pooling
    for efficient database operations
    """

    def __init__(self, config: Optional[DatabaseConfig] = None):
        """
        Initialize database connector with connection pool

        Args:
            config: DatabaseConfig object, creates default if None
        """
        self.config = config if config else DatabaseConfig()
        self.connection_pool = None
        self._initialize_pool()

    def _initialize_pool(self):
        """Initialize connection pool"""
        try:
            pool_config = self.config.to_dict()
            pool_config['pool_name'] = self.config.pool_name
            pool_config['pool_size'] = self.config.pool_size

            self.connection_pool = pooling.MySQLConnectionPool(**pool_config)
            print(f"✓ Connection pool '{self.config.pool_name}' created successfully")
        except Error as e:
            print(f"✗ Error creating connection pool: {e}")
            raise

    @contextmanager
    def get_connection(self):
        """
        Context manager to get a connection from the pool
        Ensures proper connection cleanup

        Usage:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                # perform operations
        """
        connection = None
        try:
            connection = self.connection_pool.get_connection()
            yield connection
        except Error as e:
            print(f"✗ Error getting connection from pool: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                connection.close()

    def test_connection(self) -> bool:
        """
        Test database connection

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                cursor.close()

                if result:
                    print(f"✓ Successfully connected to database '{self.config.database}'")
                    return True
                return False
        except Error as e:
            print(f"✗ Connection test failed: {e}")
            return False

    def execute_query(self, query: str, params: Optional[tuple] = None,
                     fetch: bool = False) -> Optional[List[tuple]]:
        """
        Execute a SQL query (SELECT)

        Args:
            query: SQL query string
            params: Optional tuple of parameters for parameterized query
            fetch: Whether to fetch results (True for SELECT, False for others)

        Returns:
            List of tuples if fetch=True, None otherwise
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params or ())

                if fetch:
                    results = cursor.fetchall()
                    cursor.close()
                    return results
                else:
                    conn.commit()
                    cursor.close()
                    return None

        except Error as e:
            print(f"✗ Query execution error: {e}")
            print(f"Query: {query}")
            raise

    def execute_query_dict(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results as list of dictionaries

        Args:
            query: SQL query string
            params: Optional tuple of parameters

        Returns:
            List of dictionaries with column names as keys
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query, params or ())
                results = cursor.fetchall()
                cursor.close()
                return results

        except Error as e:
            print(f"✗ Query execution error: {e}")
            raise

    def execute_many(self, query: str, data: List[tuple]) -> int:
        """
        Execute multiple INSERT/UPDATE queries efficiently

        Args:
            query: SQL query with placeholders
            data: List of tuples containing data

        Returns:
            Number of rows affected
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.executemany(query, data)
                conn.commit()
                affected_rows = cursor.rowcount
                cursor.close()
                return affected_rows

        except Error as e:
            print(f"✗ Batch execution error: {e}")
            raise

    def execute_script(self, script_path: str) -> bool:
        """
        Execute a SQL script file

        Args:
            script_path: Path to .sql file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(script_path, 'r') as f:
                sql_script = f.read()

            # Split by statements (basic implementation)
            statements = sql_script.split(';')

            with self.get_connection() as conn:
                cursor = conn.cursor()

                for statement in statements:
                    statement = statement.strip()
                    if statement and not statement.startswith('--'):
                        try:
                            cursor.execute(statement)
                        except Error as e:
                            # Skip certain errors like "empty query"
                            if "Query was empty" not in str(e):
                                print(f"Warning executing statement: {e}")

                conn.commit()
                cursor.close()

            print(f"✓ SQL script '{script_path}' executed successfully")
            return True

        except Exception as e:
            print(f"✗ Error executing script: {e}")
            return False

    def get_table_count(self, table_name: str) -> int:
        """
        Get row count for a table

        Args:
            table_name: Name of the table

        Returns:
            int: Number of rows
        """
        query = f"SELECT COUNT(*) FROM {table_name}"
        result = self.execute_query(query, fetch=True)
        return result[0][0] if result else 0

    def get_all_tables(self) -> List[str]:
        """
        Get list of all tables in the database

        Returns:
            List of table names
        """
        query = "SHOW TABLES"
        results = self.execute_query(query, fetch=True)
        return [row[0] for row in results] if results else []

    def truncate_table(self, table_name: str) -> bool:
        """
        Truncate a table (delete all rows)

        Args:
            table_name: Name of the table

        Returns:
            bool: True if successful
        """
        try:
            query = f"TRUNCATE TABLE {table_name}"
            self.execute_query(query)
            print(f"✓ Table '{table_name}' truncated successfully")
            return True
        except Error as e:
            print(f"✗ Error truncating table: {e}")
            return False

    def close_pool(self):
        """Close all connections in the pool"""
        # Connection pool doesn't have a direct close method
        # Connections are closed automatically when no longer in use
        print("✓ Connection pool cleanup completed")


def create_sample_config(output_path: str = "db_config.json"):
    """
    Create a sample database configuration file

    Args:
        output_path: Path to save the config file
    """
    sample_config = {
        "host": "localhost",
        "port": 3306,
        "database": "etf_backtester_db",
        "user": "root",
        "password": "your_password_here",
        "pool_name": "etf_pool",
        "pool_size": 5
    }

    with open(output_path, 'w') as f:
        json.dump(sample_config, f, indent=4)

    print(f"✓ Sample config file created at: {output_path}")
    print("  Please update with your actual database credentials")


# Example usage
if __name__ == "__main__":
    # Test the database connector
    print("=" * 60)
    print("Testing Database Connector Module")
    print("=" * 60)

    # Create connector with default config
    db = DatabaseConnector()

    # Test connection
    if db.test_connection():
        # Show all tables
        tables = db.get_all_tables()
        print(f"\nTables in database: {tables}")

        # Show row counts
        for table in tables:
            count = db.get_table_count(table)
            print(f"  - {table}: {count} rows")

    # Close pool
    db.close_pool()

    print("\n" + "=" * 60)
    print("Database connector test complete")
    print("=" * 60)
