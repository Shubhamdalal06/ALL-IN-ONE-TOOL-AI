import pandas as pd
import sqlite3
from pathlib import Path
from typing import Dict, List, Any, Tuple

class SQLModule:
    """Handle SQL operations and queries"""
    
    def __init__(self, db_path: str = "./data/ai_tool.db"):
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    def create_table_from_dataframe(self, df: pd.DataFrame, table_name: str) -> str:
        """Create SQL table from dataframe"""
        conn = sqlite3.connect(self.db_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        return f"Table '{table_name}' created successfully"
    
    def execute_query(self, query: str) -> Tuple[pd.DataFrame, str]:
        """Execute SQL query and return results"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df, "Query executed successfully"
        except Exception as e:
            return None, f"Error executing query: {str(e)}"
    
    def filter_data(self, table_name: str, conditions: Dict[str, Any]) -> pd.DataFrame:
        """Filter table by conditions"""
        conn = sqlite3.connect(self.db_path)
        
        where_clause = " AND ".join([f"{k} = '{v}'" for k, v in conditions.items()])
        query = f"SELECT * FROM {table_name} WHERE {where_clause}"
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def join_tables(self, table1: str, table2: str, on: str, 
                   join_type: str = 'INNER') -> pd.DataFrame:
        """Join two tables"""
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM {table1} {join_type} JOIN {table2} ON {table1}.{on} = {table2}.{on}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def aggregate_data(self, table_name: str, group_by: str, 
                      agg_column: str, agg_func: str) -> pd.DataFrame:
        """Aggregate data with GROUP BY"""
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT {group_by}, {agg_func}({agg_column}) as result FROM {table_name} GROUP BY {group_by}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def list_tables(self) -> List[str]:
        """List all tables in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
