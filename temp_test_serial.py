from backend.modules.file_loader import FileLoader
from backend.modules.cleaning_module import CleaningModule
from backend.modules.excel_module import ExcelModule
import pandas as pd

print('Creating test DataFrame...')
df = pd.DataFrame({'a':[1,2,2], 'b':['x', None, 'z']})

info = FileLoader.get_dataframe_info(df)
print('DataFrame info:', info)

qr = CleaningModule.get_quality_report(df)
print('Quality report:', qr)

issues = ExcelModule.validate_spreadsheet(df)
print('Spreadsheet issues:', issues)

print('All tests completed')
