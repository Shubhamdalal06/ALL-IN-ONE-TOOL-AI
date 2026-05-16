import pandas as pd
from typing import List, Dict, Any
import os
import json
from pathlib import Path

class SheetsModule:
    """Handle Google Sheets operations"""
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    def __init__(self, credentials_path: str = None):
        self.credentials_path = credentials_path or os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
        self.service = None
    
    def authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            from googleapiclient.discovery import build
            # Lazy import Credentials to avoid import-time errors when package is not installed
            from google.oauth2.service_account import Credentials as ServiceAccountCredentials

            if not self.credentials_path:
                print("Google Sheets credentials path not set (GOOGLE_SHEETS_CREDENTIALS_PATH)")
                return False

            cred_path = Path(self.credentials_path)
            # Support either a path to a service account JSON file or a JSON string in the env var
            if cred_path.is_file():
                creds = ServiceAccountCredentials.from_service_account_file(
                    str(cred_path), scopes=self.SCOPES)
            else:
                # Try parsing credential JSON from environment variable
                try:
                    cred_info = json.loads(self.credentials_path)
                    creds = ServiceAccountCredentials.from_service_account_info(cred_info, scopes=self.SCOPES)
                except Exception:
                    raise FileNotFoundError(f"Credentials file not found: {self.credentials_path}")

            self.service = build('sheets', 'v4', credentials=creds)
            return True
        except Exception as e:
            print(f"Authentication failed: {str(e)}")
            return False
    
    def read_sheet(self, sheet_id: str, sheet_name: str = 'Sheet1') -> pd.DataFrame:
        """Read data from Google Sheet"""
        if not self.service:
            ok = self.authenticate()
            if not ok:
                raise RuntimeError("Google Sheets authentication failed. Check credentials and logs.")
        
        try:
            from googleapiclient.discovery import build
            result = self.service.spreadsheets().values().get(
                spreadsheetId=sheet_id,
                range=sheet_name
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return pd.DataFrame()
            
            df = pd.DataFrame(values[1:], columns=values[0])
            return df
        except Exception as e:
            print(f"Error reading sheet: {str(e)}")
            return pd.DataFrame()
    
    def write_sheet(self, sheet_id: str, sheet_name: str, 
                   df: pd.DataFrame) -> str:
        """Write data to Google Sheet"""
        if not self.service:
            ok = self.authenticate()
            if not ok:
                return "Authentication failed: unable to write to Google Sheets"
        
        try:
            values = [df.columns.tolist()] + df.values.tolist()
            
            self.service.spreadsheets().values().update(
                spreadsheetId=sheet_id,
                range=sheet_name,
                valueInputOption='RAW',
                body={'values': values}
            ).execute()
            
            return f"Data written to {sheet_name}"
        except Exception as e:
            return f"Error writing to sheet: {str(e)}"
    
    def append_sheet(self, sheet_id: str, sheet_name: str, 
                    df: pd.DataFrame) -> str:
        """Append data to Google Sheet"""
        if not self.service:
            ok = self.authenticate()
            if not ok:
                return "Authentication failed: unable to append to Google Sheets"
        
        try:
            values = df.values.tolist()
            
            self.service.spreadsheets().values().append(
                spreadsheetId=sheet_id,
                range=sheet_name,
                valueInputOption='RAW',
                body={'values': values}
            ).execute()
            
            return f"Data appended to {sheet_name}"
        except Exception as e:
            return f"Error appending to sheet: {str(e)}"
    
    def sync_with_excel(self, df: pd.DataFrame, sheet_id: str, 
                       sheet_name: str) -> str:
        """Sync Excel data with Google Sheet"""
        return self.write_sheet(sheet_id, sheet_name, df)
