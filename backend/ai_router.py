import os
from anthropic import Anthropic
from typing import Dict, Any, List
import json

class AIRouter:
    """
    AI-powered task router using Claude API
    Interprets user commands and routes to appropriate modules
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = Anthropic()
        self.conversation_history = []
        
        self.system_prompt = """You are an AI assistant for data analysis and processing. Your job is to:

1. Understand what the user wants to do with their data
2. Route them to the appropriate tool module
3. Generate specific instructions for the selected module

Available modules:
- EXCEL_MODULE: For pivot tables, formulas, spreadsheet operations, summary statistics, formatting
- SQL_MODULE: For queries, filtering, joining tables, aggregations, data retrieval
- SHEETS_MODULE: For Google Sheets operations, syncing data, reading/writing sheets
- SIXSIGMA_MODULE: For quality analysis, Pareto analysis, control charts, capability analysis, hypothesis testing
- CLEANING_MODULE: For removing duplicates, handling missing values, removing outliers, data normalization, text cleaning

When the user asks for a task:
1. Identify the primary module needed
2. Provide the specific function to use
3. Include any required parameters
4. Suggest relevant follow-up analyses

Always respond in this JSON format:
{
    "module": "MODULE_NAME",
    "function": "function_name",
    "parameters": {required parameters},
    "reasoning": "Why this module is best",
    "suggested_next_steps": ["optional follow-ups"]
}"""
    
    def interpret_command(self, user_message: str, dataframe_info: Dict = None) -> Dict[str, Any]:
        """
        Use Claude to interpret user command and route to modules
        """
        # Add dataframe context if available
        context = ""
        if dataframe_info:
            context = f"\nCurrent data: {dataframe_info['rows']} rows, {dataframe_info['columns']} columns\n"
            context += f"Columns: {', '.join(dataframe_info['column_names'])}\n"
        
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message + context
        })
        
        # Get response from Claude
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        # Parse the response
        try:
            # Try to extract JSON from the response
            json_start = assistant_message.find('{')
            json_end = assistant_message.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = assistant_message[json_start:json_end]
                result = json.loads(json_str)
                return result
        except json.JSONDecodeError:
            pass
        
        # If JSON parsing fails, return structured response
        return {
            "module": "UNKNOWN",
            "function": "unknown",
            "parameters": {},
            "reasoning": assistant_message,
            "raw_response": assistant_message
        }
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_routing_suggestion(self, keywords: List[str]) -> str:
        """
        Quick routing based on keywords (fallback method)
        """
        routing_map = {
            'chart': 'EXCEL_MODULE',
            'pivot': 'EXCEL_MODULE',
            'formula': 'EXCEL_MODULE',
            'summary': 'EXCEL_MODULE',
            'query': 'SQL_MODULE',
            'filter': 'SQL_MODULE',
            'join': 'SQL_MODULE',
            'aggregate': 'SQL_MODULE',
            'sheets': 'SHEETS_MODULE',
            'google': 'SHEETS_MODULE',
            'sync': 'SHEETS_MODULE',
            'pareto': 'SIXSIGMA_MODULE',
            'six sigma': 'SIXSIGMA_MODULE',
            'control': 'SIXSIGMA_MODULE',
            'capability': 'SIXSIGMA_MODULE',
            'clean': 'CLEANING_MODULE',
            'duplicate': 'CLEANING_MODULE',
            'outlier': 'CLEANING_MODULE',
            'normalize': 'CLEANING_MODULE',
            'missing': 'CLEANING_MODULE',
        }
        
        for keyword in keywords:
            for key, module in routing_map.items():
                if key.lower() in keyword.lower():
                    return module
        
        return "UNKNOWN"
