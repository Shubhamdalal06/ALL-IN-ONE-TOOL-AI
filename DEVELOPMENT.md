# Development Guide

Learn how to extend and customize the AI All-in-One Tool.

## Creating Custom Modules

### Module Structure

Each module follows this pattern:

```python
from typing import Dict, List, Any, Tuple
import pandas as pd

class CustomModule:
    """Description of what your module does"""
    
    @staticmethod
    def main_function(df: pd.DataFrame, param1: str, param2: int = 10) -> Any:
        """
        Main function that processes data
        
        Args:
            df: Input dataframe
            param1: Parameter description
            param2: Optional parameter with default
            
        Returns:
            Processed result
        """
        # Your implementation
        result = df.groupby(param1).sum()
        return result
    
    @staticmethod
    def helper_function(df: pd.DataFrame) -> Dict:
        """Helper function"""
        return {"info": "processed"}
```

### Step-by-Step: Create a Statistics Module

#### 1. Create the Module File

```python
# backend/modules/stats_module.py
import pandas as pd
import numpy as np
from scipy import stats as scipy_stats

class StatsModule:
    """Advanced statistical analysis"""
    
    @staticmethod
    def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate correlation matrix for numeric columns"""
        numeric_df = df.select_dtypes(include=[np.number])
        return numeric_df.corr()
    
    @staticmethod
    def distribution_test(df: pd.DataFrame, column: str) -> Dict:
        """Test if data is normally distributed"""
        data = df[column].dropna()
        stat, p_value = scipy_stats.shapiro(data)
        
        return {
            "test": "Shapiro-Wilk",
            "statistic": round(stat, 4),
            "p_value": round(p_value, 4),
            "is_normal": p_value > 0.05,
            "interpretation": "Data is normally distributed" if p_value > 0.05 else "Data is NOT normally distributed"
        }
    
    @staticmethod
    def regression_analysis(df: pd.DataFrame, x_col: str, y_col: str) -> Dict:
        """Simple linear regression"""
        x = df[x_col].values.reshape(-1, 1)
        y = df[y_col].values
        
        slope = np.polyfit(x.flatten(), y, 1)[0]
        intercept = np.polyfit(x.flatten(), y, 1)[1]
        
        return {
            "slope": round(slope, 4),
            "intercept": round(intercept, 4),
            "equation": f"y = {intercept:.4f} + {slope:.4f}x"
        }
```

#### 2. Register in AI Router

Edit `backend/ai_router.py` and add to system prompt:

```python
"""
...existing modules...
- STATS_MODULE: For correlation, regression, distribution tests
"""
```

#### 3. Add API Endpoint

Edit `backend/main.py`:

```python
from modules.stats_module import StatsModule

stats_module = StatsModule()

@app.post("/stats/correlation")
async def get_correlation(file_id: str = Form(...)):
    """Calculate correlation matrix"""
    if file_id not in uploaded_data:
        raise HTTPException(status_code=404, detail="File not found")
    
    df = uploaded_data[file_id]
    corr_matrix = stats_module.correlation_matrix(df)
    
    return {
        "success": True,
        "correlation": corr_matrix.to_dict()
    }
```

#### 4. Update Documentation

Add to `README.md`:

```markdown
### Stats Module
- Correlation analysis
- Distribution testing
- Regression analysis
- Time series analysis
```

## Modifying AI Router Behavior

### Update Routing Logic

Edit `backend/ai_router.py`:

```python
def __init__(self):
    # Add more specific routing instructions
    self.system_prompt = """
    ...
    When user mentions:
    - "correlation", "regression" → STATS_MODULE
    - "distribution", "normal" → STATS_MODULE
    ...
    """
```

### Add Custom Keywords

```python
def get_routing_suggestion(self, keywords: List[str]) -> str:
    routing_map = {
        # ... existing mappings
        'correlation': 'STATS_MODULE',
        'regression': 'STATS_MODULE',
        'normal': 'STATS_MODULE',
    }
    # ... rest of function
```

## Extending Frontend

### Add New UI Section

Edit `frontend/index.html`:

```html
<!-- Add new panel -->
<div class="panel">
    <h2>📊 Statistics</h2>
    
    <div class="form-group">
        <label>Select Column for Analysis:</label>
        <select id="columnSelect">
            <option value="">Loading columns...</option>
        </select>
    </div>
    
    <button onclick="analyzeStats()">Analyze</button>
    
    <div id="statsResults"></div>
</div>
```

### Add JavaScript Handler

```javascript
async function analyzeStats() {
    if (!currentFileId) {
        showStatus('processStatus', 'Please upload a file', 'error');
        return;
    }
    
    const column = document.getElementById('columnSelect').value;
    
    const formData = new FormData();
    formData.append('file_id', currentFileId);
    formData.append('column', column);
    
    try {
        const response = await fetch(`${API_BASE}/stats/analyze`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        document.getElementById('statsResults').innerHTML = 
            `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    } catch (error) {
        showStatus('processStatus', `Error: ${error.message}`, 'error');
    }
}
```

## Database Enhancements

### Switch to PostgreSQL

1. Install PostgreSQL driver:
```bash
pip install psycopg2-binary sqlalchemy
```

2. Update `sql_module.py`:

```python
from sqlalchemy import create_engine

class SQLModule:
    def __init__(self, db_url: str = None):
        # SQLite
        # self.engine = create_engine('sqlite:///data/ai_tool.db')
        
        # PostgreSQL
        self.engine = create_engine(
            'postgresql://user:password@localhost/ai_tool'
        )
```

### Add Authentication

```python
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, DateTime

# Create users table
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

## Testing

### Unit Tests

Create `backend/tests/test_modules.py`:

```python
import unittest
import pandas as pd
from modules.excel_module import ExcelModule

class TestExcelModule(unittest.TestCase):
    
    def setUp(self):
        self.df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })
    
    def test_create_pivot(self):
        result = ExcelModule.create_pivot_table(
            self.df, index='A'
        )
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_summary(self):
        result = ExcelModule.create_summary(self.df)
        self.assertEqual(result.shape[0], 8)  # 8 stats rows

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m pytest backend/tests/
```

## Performance Optimization

### 1. Add Caching

```python
from functools import lru_cache

class ExcelModule:
    @staticmethod
    @lru_cache(maxsize=128)
    def cached_pivot_table(df: pd.DataFrame, index: str):
        return df.pivot_table(index=index)
```

### 2. Async Processing

```python
from fastapi import BackgroundTasks
import asyncio

@app.post("/process-async")
async def process_async(
    file_id: str = Form(...),
    background_tasks: BackgroundTasks = None
):
    background_tasks.add_task(heavy_computation, file_id)
    return {"message": "Processing started"}

async def heavy_computation(file_id: str):
    # Long-running operation
    df = uploaded_data[file_id]
    result = await long_operation(df)
```

### 3. Batch Processing

```python
def process_batch(df: pd.DataFrame, batch_size: int = 1000):
    """Process data in chunks"""
    for i in range(0, len(df), batch_size):
        batch = df[i:i+batch_size]
        yield process_chunk(batch)
```

## Deployment

### Docker Setup

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "backend/main.py"]
```

Build and run:
```bash
docker build -t ai-tool .
docker run -p 8000:8000 -e ANTHROPIC_API_KEY=your_key ai-tool
```

### Environment Variables

```bash
# Production
ANTHROPIC_API_KEY=sk-...
DATABASE_PATH=/data/ai_tool.db
SERVER_PORT=8000
DEBUG=false
```

## Common Tasks

### Add a New Data Format

```python
# In file_loader.py
def load_file(self, file_path: str):
    # ... existing formats ...
    elif extension == '.parquet':
        df = pd.read_parquet(file_path)
        return df, 'parquet'
```

### Add Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info(f"Processing file: {filename}")
logger.error(f"Error: {str(e)}")
```

### Add Error Tracking

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)

@app.post("/process")
async def process_data(...):
    try:
        # ... processing
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise
```

## Troubleshooting Development

### Module Not Found
```bash
# Make sure module is in backend/modules/
# Add to __init__.py
python -c "from modules.your_module import YourModule"
```

### API Not Responding
```bash
# Check if server is running
curl http://localhost:8000

# Check logs for errors
python backend/main.py
```

### Dataframe Issues
```python
# Debug dataframe state
print(df.head())
print(df.dtypes)
print(df.info())
print(df.describe())
```

## Best Practices

1. **Type Hints**: Always use type hints for function parameters
2. **Docstrings**: Document all functions with docstrings
3. **Error Handling**: Use try-except with specific exceptions
4. **Testing**: Write tests for critical functions
5. **Logging**: Log important operations and errors
6. **Performance**: Profile code for bottlenecks
7. **Security**: Validate all inputs
8. **Documentation**: Keep README updated with changes

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Anthropic API](https://docs.anthropic.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
