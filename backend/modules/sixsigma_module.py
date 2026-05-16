import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from typing import Dict, Tuple, Any
import io

class SixSigmaModule:
    """Six Sigma and quality analysis tools (DMAIC methodology)"""
    
    @staticmethod
    def pareto_analysis(df: pd.DataFrame, defect_column: str, 
                       count_column: str = None) -> Tuple[pd.DataFrame, str]:
        """
        Perform Pareto analysis (80/20 rule)
        Identifies vital few defects causing most issues
        """
        if count_column is None:
            data = df[defect_column].value_counts().reset_index()
            data.columns = ['Defect', 'Count']
        else:
            data = df.groupby(defect_column)[count_column].sum().reset_index()
            data.columns = ['Defect', 'Count']
        
        data = data.sort_values('Count', ascending=False)
        data['Cumulative'] = data['Count'].cumsum()
        data['Cumulative %'] = (data['Cumulative'] / data['Count'].sum() * 100).round(2)
        
        vital_few = data[data['Cumulative %'] <= 80]
        
        return data, f"Vital {len(vital_few)} defects cause ~80% of issues"
    
    @staticmethod
    def control_chart_analysis(df: pd.DataFrame, value_column: str, 
                              sample_size: int = 5) -> Dict[str, Any]:
        """
        Create control chart data (X-bar and R charts)
        """
        mean = df[value_column].mean()
        std = df[value_column].std()
        
        # Calculate control limits (3-sigma)
        ucl = mean + (3 * std)
        lcl = mean - (3 * std)
        
        out_of_control = df[(df[value_column] > ucl) | (df[value_column] < lcl)]
        
        return {
            "mean": mean,
            "std_dev": std,
            "upper_control_limit": ucl,
            "lower_control_limit": lcl,
            "out_of_control_points": len(out_of_control),
            "capability_ratio": (ucl - lcl) / (6 * std) if std > 0 else 0
        }
    
    @staticmethod
    def process_capability_index(df: pd.DataFrame, value_column: str, 
                                 lower_spec: float, upper_spec: float) -> Dict[str, float]:
        """
        Calculate Cpk (Process Capability Index)
        Measures how well process meets specifications
        """
        mean = df[value_column].mean()
        std = df[value_column].std()
        
        if std == 0:
            return {"error": "Standard deviation is zero"}
        
        cpu = (upper_spec - mean) / (3 * std)
        cpl = (mean - lower_spec) / (3 * std)
        cpk = min(cpu, cpl)
        
        interpretation = "Process capable" if cpk >= 1.33 else "Process needs improvement"
        
        return {
            "Cpk": round(cpk, 3),
            "Cpu": round(cpu, 3),
            "Cpl": round(cpl, 3),
            "interpretation": interpretation
        }
    
    @staticmethod
    def hypothesis_test(df: pd.DataFrame, column: str, 
                       test_type: str = 'normality') -> Dict[str, Any]:
        """
        Perform hypothesis tests (normality, t-test, etc.)
        """
        if test_type == 'normality':
            stat, p_value = stats.shapiro(df[column].dropna())
            return {
                "test": "Shapiro-Wilk Normality Test",
                "statistic": round(stat, 4),
                "p_value": round(p_value, 4),
                "is_normal": "Yes" if p_value > 0.05 else "No"
            }
        elif test_type == 'variance':
            groups = df.groupby(df.columns[0])[column].apply(list).values
            stat, p_value = stats.f_oneway(*groups)
            return {
                "test": "ANOVA Test",
                "statistic": round(stat, 4),
                "p_value": round(p_value, 4),
                "significant_difference": "Yes" if p_value < 0.05 else "No"
            }
        
        return {"error": "Unknown test type"}
    
    @staticmethod
    def generate_report(df: pd.DataFrame, metric_column: str, 
                       defect_column: str = None) -> str:
        """Generate Six Sigma summary report"""
        report = f"""
=== SIX SIGMA ANALYSIS REPORT ===
Total Records: {len(df)}
Mean: {df[metric_column].mean():.2f}
Std Dev: {df[metric_column].std():.2f}
Min: {df[metric_column].min():.2f}
Max: {df[metric_column].max():.2f}

Quartiles:
Q1: {df[metric_column].quantile(0.25):.2f}
Q2 (Median): {df[metric_column].quantile(0.50):.2f}
Q3: {df[metric_column].quantile(0.75):.2f}

Distribution: {'Right Skewed' if df[metric_column].skew() > 0 else 'Left Skewed' if df[metric_column].skew() < 0 else 'Symmetric'}
        """
        return report
