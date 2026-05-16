import pandas as pd
import openpyxl
from pathlib import Path
from typing import Optional, Tuple
import io

class FileLoader:
    """Load and manage different file types (Excel, CSV, etc.)"""
    
    @staticmethod
    def load_file(file_path: str) -> Tuple[pd.DataFrame, str]:
        """
        Load a file and return dataframe and file type
        
        Args:
            file_path: Path to the file
            
        Returns:
            Tuple of (dataframe, file_type)
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension == '.xlsx' or extension == '.xls':
            df = pd.read_excel(file_path)
            return df, 'excel'
        elif extension == '.csv':
            df = pd.read_csv(file_path)
            return df, 'csv'
        elif extension == '.json':
            df = pd.read_json(file_path)
            return df, 'json'
        else:
            raise ValueError(f"Unsupported file type: {extension}")
    
    @staticmethod
    def load_from_bytes(file_bytes: bytes, filename: str) -> Tuple[pd.DataFrame, str]:
        """Load file from bytes (from upload)"""
        extension = Path(filename).suffix.lower()
        
        if extension == '.xlsx' or extension == '.xls':
            df = pd.read_excel(io.BytesIO(file_bytes))
            return df, 'excel'
        elif extension == '.csv':
            df = pd.read_csv(io.BytesIO(file_bytes))
            return df, 'csv'
        elif extension == '.json':
            df = pd.read_json(io.BytesIO(file_bytes))
            return df, 'json'
        else:
            raise ValueError(f"Unsupported file type: {extension}")
    
    @staticmethod
    def save_excel(df: pd.DataFrame, output_path: str) -> str:
        """Save dataframe to Excel"""
        df.to_excel(output_path, index=False)
        return output_path
    
    @staticmethod
    def get_dataframe_info(df: pd.DataFrame) -> dict:
        """Get metadata about dataframe"""
        # Convert dtypes and numeric numpy types to plain Python types for JSON serialization
        dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
        memory = df.memory_usage(deep=True).sum()
        try:
            memory = int(memory)
        except Exception:
            memory = float(memory)

        return {
            "rows": int(len(df)),
            "columns": int(len(df.columns)),
            "column_names": [str(c) for c in df.columns.tolist()],
            "dtypes": dtypes,
            "memory_usage": memory
        }
