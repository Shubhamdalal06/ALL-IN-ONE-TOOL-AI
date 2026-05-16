import pandas as pd
import numpy as np
from typing import Dict, Tuple, List

class CleaningModule:
    """Data cleaning and preprocessing operations"""
    
    @staticmethod
    def remove_duplicates(df: pd.DataFrame, subset: List[str] = None) -> Tuple[pd.DataFrame, str]:
        """Remove duplicate rows"""
        initial_count = len(df)
        df_clean = df.drop_duplicates(subset=subset)
        removed = initial_count - len(df_clean)
        
        return df_clean, f"Removed {removed} duplicate rows"
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, strategy: str = 'drop', 
                             column: str = None) -> Tuple[pd.DataFrame, str]:
        """
        Handle missing values
        strategy: 'drop', 'fill_mean', 'fill_median', 'fill_forward', 'fill_backward'
        """
        if strategy == 'drop':
            df_clean = df.dropna()
            return df_clean, f"Dropped rows with missing values"
        elif strategy == 'fill_mean':
            df_clean = df.fillna(df.mean(numeric_only=True))
            return df_clean, "Filled missing values with mean"
        elif strategy == 'fill_median':
            df_clean = df.fillna(df.median(numeric_only=True))
            return df_clean, "Filled missing values with median"
        elif strategy == 'fill_forward':
            df_clean = df.fillna(method='ffill')
            return df_clean, "Filled missing values forward"
        elif strategy == 'fill_backward':
            df_clean = df.fillna(method='bfill')
            return df_clean, "Filled missing values backward"
        
        return df, "No changes made"
    
    @staticmethod
    def remove_outliers(df: pd.DataFrame, column: str, 
                       method: str = 'iqr') -> Tuple[pd.DataFrame, str]:
        """
        Remove outliers using IQR or Z-score
        """
        if method == 'iqr':
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            
            df_clean = df[(df[column] >= Q1 - 1.5 * IQR) & (df[column] <= Q3 + 1.5 * IQR)]
            removed = len(df) - len(df_clean)
            return df_clean, f"Removed {removed} outliers using IQR method"
        
        elif method == 'zscore':
            z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
            df_clean = df[z_scores < 3]
            removed = len(df) - len(df_clean)
            return df_clean, f"Removed {removed} outliers using Z-score method"
        
        return df, "No changes made"
    
    @staticmethod
    def normalize_column(df: pd.DataFrame, column: str, 
                        method: str = 'minmax') -> pd.DataFrame:
        """
        Normalize column
        method: 'minmax' (0-1) or 'zscore' (standardize)
        """
        if method == 'minmax':
            min_val = df[column].min()
            max_val = df[column].max()
            df[f'{column}_normalized'] = (df[column] - min_val) / (max_val - min_val)
        elif method == 'zscore':
            mean = df[column].mean()
            std = df[column].std()
            df[f'{column}_normalized'] = (df[column] - mean) / std
        
        return df
    
    @staticmethod
    def fix_data_types(df: pd.DataFrame) -> Tuple[pd.DataFrame, str]:
        """
        Auto-detect and fix data types
        """
        for column in df.columns:
            if df[column].dtype == 'object':
                # Try to convert to numeric
                try:
                    df[column] = pd.to_numeric(df[column])
                except:
                    # Try to convert to datetime
                    try:
                        df[column] = pd.to_datetime(df[column])
                    except:
                        pass
        
        return df, "Data types corrected"
    
    @staticmethod
    def handle_text_data(df: pd.DataFrame, column: str, 
                        operation: str = 'lower') -> pd.DataFrame:
        """
        Text cleaning operations
        operation: 'lower', 'upper', 'strip', 'remove_special'
        """
        if operation == 'lower':
            df[column] = df[column].str.lower()
        elif operation == 'upper':
            df[column] = df[column].str.upper()
        elif operation == 'strip':
            df[column] = df[column].str.strip()
        elif operation == 'remove_special':
            df[column] = df[column].str.replace('[^a-zA-Z0-9 ]', '', regex=True)
        
        return df
    
    @staticmethod
    def get_quality_report(df: pd.DataFrame) -> Dict:
        """Generate data quality report"""
        missing = df.isnull().sum().to_dict()
        missing = {str(k): int(v) for k, v in missing.items()}

        dtypes = {str(k): str(v) for k, v in df.dtypes.items()}

        mem = df.memory_usage(deep=True).sum()
        try:
            mem_mb = round(int(mem) / 1024 / 1024, 2)
        except Exception:
            mem_mb = round(float(mem) / 1024 / 1024, 2)

        report = {
            "total_rows": int(len(df)),
            "total_columns": int(len(df.columns)),
            "missing_values": missing,
            "duplicates": int(len(df[df.duplicated()])),
            "data_types": dtypes,
            "memory_usage_mb": mem_mb
        }
        return report
