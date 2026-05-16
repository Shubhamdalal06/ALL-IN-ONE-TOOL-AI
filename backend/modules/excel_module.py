import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill
from io import BytesIO
from typing import Dict, Any, List

class ExcelModule:
    """Handle Excel operations: formulas, pivots, charts, formatting"""
    
    @staticmethod
    def create_pivot_table(df: pd.DataFrame, index: str, columns: str = None, 
                          values: str = None, aggfunc: str = 'sum') -> pd.DataFrame:
        """Create pivot table"""
        return df.pivot_table(index=index, columns=columns, values=values, aggfunc=aggfunc)
    
    @staticmethod
    def add_formula(df: pd.DataFrame, column_name: str, formula_type: str, 
                   target_column: str) -> pd.DataFrame:
        """
        Add calculated columns with common formulas
        
        formula_type: 'sum', 'avg', 'count', 'max', 'min', 'custom'
        """
        if formula_type == 'sum':
            df[column_name] = df[target_column].sum()
        elif formula_type == 'avg':
            df[column_name] = df[target_column].mean()
        elif formula_type == 'count':
            df[column_name] = df[target_column].count()
        elif formula_type == 'max':
            df[column_name] = df[target_column].max()
        elif formula_type == 'min':
            df[column_name] = df[target_column].min()
        
        return df
    
    @staticmethod
    def create_summary(df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
        """Create summary statistics"""
        if columns is None:
            columns = df.select_dtypes(include=['number']).columns.tolist()
        
        summary = df[columns].describe()
        return summary
    
    @staticmethod
    def save_with_formatting(df: pd.DataFrame, output_path: str, 
                            title: str = "Data Report") -> str:
        """Save Excel with formatting"""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)
            
            # Access workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['Data']
            
            # Format header
            header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF")
            
            for cell in worksheet[1]:
                cell.fill = header_fill
                cell.font = header_font
        
        return output_path
    
    @staticmethod
    def validate_spreadsheet(df: pd.DataFrame) -> Dict[str, Any]:
        """Check for data quality issues"""
        missing = df.isnull().sum().to_dict()
        # convert numpy ints to int for JSON
        missing = {str(k): int(v) for k, v in missing.items()}

        dtypes = {str(k): str(v) for k, v in df.dtypes.items()}

        issues = {
            "missing_values": missing,
            "duplicates": int(len(df[df.duplicated()])),
            "empty_columns": [str(col) for col in df.columns if df[col].isnull().all()],
            "data_types": dtypes
        }
        return issues
