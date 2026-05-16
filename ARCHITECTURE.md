# Architecture & Technical Details

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Browser UI                           │
│              (HTML/Vanilla JavaScript)                  │
└────────────┬────────────────────────────────────────────┘
             │ HTTP/REST API
┌────────────▼────────────────────────────────────────────┐
│                   FastAPI Backend                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │  AI Router (Claude-powered)                      │   │
│  │  - Interprets user commands                      │   │
│  │  - Routes to correct module                      │   │
│  │  - Maintains conversation context                │   │
│  └────────────────────────────────────────────────┘   │
└────────────┬─────────────────────────────────────────────┘
             │
    ┌────────┴────────┬──────────────┬──────────────┐
    │                 │              │              │
┌───▼────────┐   ┌────▼──────┐  ┌───▼──────┐  ┌───▼──────┐
│   Excel    │   │    SQL    │  │ Cleaning │  │SixSigma  │
│  Module    │   │  Module   │  │  Module  │  │ Module   │
└────────────┘   └───────────┘  └──────────┘  └──────────┘
    │
    ├─ Pivot Tables
    ├─ Formulas
    ├─ Summaries
    └─ Formatting


    │                   │
    ├─ Queries      ├─ Duplicates
    ├─ Filtering    ├─ Missing Values
    ├─ Joins        ├─ Outliers
    └─ Aggregations └─ Normalization


                       │
                       ├─ Pareto Analysis
                       ├─ Control Charts
                       ├─ Cpk Index
                       └─ Hypothesis Tests

                  ┌─────────────────┐
                  │  Data Storage   │
                  │  SQLite DB      │
                  └─────────────────┘
```

## Data Flow

### 1. File Upload
```
User Upload → FastAPI Endpoint → FileLoader → DataFrame → Memory Storage
```

### 2. Command Processing
```
User Command → AI Router (Claude) → Module Selection → Module Execution → Result
```

### 3. Data Export
```
Processed DataFrame → Excel Formatter → File Generation → Download
```

## Module Details

### Excel Module
**Location:** `backend/modules/excel_module.py`

**Functions:**
- `create_pivot_table()` - Multi-dimensional data summary
- `add_formula()` - Add calculated columns
- `create_summary()` - Statistical summary
- `save_with_formatting()` - Formatted Excel export
- `validate_spreadsheet()` - Quality check

**Use Cases:**
- Dashboard creation
- Report generation
- Data aggregation
- Performance metrics

### SQL Module
**Location:** `backend/modules/sql_module.py`

**Functions:**
- `create_table_from_dataframe()` - Load data to SQLite
- `execute_query()` - Run custom SQL
- `filter_data()` - WHERE clause filtering
- `join_tables()` - JOIN operations
- `aggregate_data()` - GROUP BY aggregations
- `list_tables()` - Database introspection

**Use Cases:**
- Complex queries
- Data joins
- Filtering large datasets
- Multi-table analysis

### Cleaning Module
**Location:** `backend/modules/cleaning_module.py`

**Functions:**
- `remove_duplicates()` - Deduplicate rows
- `handle_missing_values()` - Fill/drop NA values
- `remove_outliers()` - IQR or Z-score method
- `normalize_column()` - MinMax or Z-score normalization
- `fix_data_types()` - Auto type detection
- `handle_text_data()` - Text preprocessing
- `get_quality_report()` - Data health metrics

**Use Cases:**
- Data preprocessing
- Data quality assurance
- Feature engineering
- Preparing ML models

### Six Sigma Module
**Location:** `backend/modules/sixsigma_module.py`

**Functions:**
- `pareto_analysis()` - 80/20 analysis
- `control_chart_analysis()` - X-bar & R charts
- `process_capability_index()` - Cpk calculation
- `hypothesis_test()` - Statistical tests
- `generate_report()` - Summary statistics

**Use Cases:**
- Quality management
- Process improvement
- Root cause analysis
- Performance metrics

### Google Sheets Module
**Location:** `backend/modules/sheets_module.py`

**Functions:**
- `authenticate()` - OAuth setup
- `read_sheet()` - Read from Google Sheets
- `write_sheet()` - Write to Google Sheets
- `append_sheet()` - Append data
- `sync_with_excel()` - Bidirectional sync

**Use Cases:**
- Cloud collaboration
- Real-time data sync
- Team reporting
- Dashboard publishing

### AI Router
**Location:** `backend/ai_router.py`

**Features:**
- Claude-powered command interpretation
- Context-aware routing
- Conversation memory
- Parameter extraction
- Fallback keyword routing

**How It Works:**
1. User provides natural language command
2. Router sends to Claude with module descriptions
3. Claude selects best module + parameters
4. Response parsed from JSON
5. Appropriate module executed

## API Endpoints

### Core Endpoints

#### Upload File
```
POST /upload
Content-Type: multipart/form-data

Parameters:
- file: File (binary)

Response:
{
  "success": true,
  "file_id": "data_xlsx",
  "file_type": "excel",
  "info": {
    "rows": 1000,
    "columns": 15,
    "column_names": [...]
  }
}
```

#### Process Data
```
POST /process
Content-Type: application/x-www-form-urlencoded

Parameters:
- file_id: string
- user_command: string
- module_hint: string (optional)

Response:
{
  "success": true,
  "routing": {
    "module": "EXCEL_MODULE",
    "function": "create_pivot_table",
    "parameters": {...}
  },
  "result": {...}
}
```

#### Download File
```
POST /download
Content-Type: application/x-www-form-urlencoded

Parameters:
- file_id: string
- format: string (excel|csv)

Response:
Binary file (Excel/CSV)
```

### Module-Specific Endpoints

```
POST /excel/pivot
POST /excel/summary
POST /cleaning/remove-duplicates
POST /cleaning/handle-missing
POST /sixsigma/pareto
POST /sixsigma/control-chart
```

## Database Schema

### SQLite Database (`data/ai_tool.db`)

Tables are dynamically created from uploaded data:

```sql
-- Example: Sales data
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    date TEXT,
    product TEXT,
    region TEXT,
    amount REAL,
    quantity INTEGER
);
```

## Configuration Files

### .env
Environment variables for API keys and settings:
```
ANTHROPIC_API_KEY=sk-...
DATABASE_PATH=./data/ai_tool.db
SERVER_PORT=8000
```

### requirements.txt
Python package dependencies:
```
fastapi==0.104.1
pandas==2.1.1
anthropic==0.7.0
...
```

## Error Handling

### File Upload Errors
```python
# Unsupported file type
{"error": "Unsupported file type: .txt"}

# File read error
{"error": "Error reading file: file may be corrupted"}
```

### API Errors
```python
# Missing file
{"detail": "File not found"}

# Processing error
{"detail": "Error processing data: ..."}
```

## Performance Considerations

### Data Size Limits
- Single file: Up to 500MB (configurable)
- DataFrame in memory: System RAM dependent
- Database: SQLite scales to ~1GB

### Optimization Tips
1. **Large Files**: Use SQL module for filtering
2. **Many Columns**: Select needed columns early
3. **Aggregations**: Use SQL GROUP BY for large data
4. **Parallel Processing**: Implement with `concurrent.futures`

## Security Considerations

### Current Implementation
- CORS enabled for all origins (development)
- No authentication
- API keys in environment variables
- Files stored in memory

### Production Recommendations
1. Add API authentication (JWT tokens)
2. Implement rate limiting
3. Restrict CORS to specific domains
4. Use environment-based secrets management
5. Add request validation/sanitization
6. Implement audit logging
7. Use HTTPS only
8. Add file upload size limits
9. Implement input validation for SQL

## Deployment

### Local Development
```bash
python main.py
```

### Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Cloud Platforms
- **Heroku**: Add `Procfile`, deploy with git
- **AWS**: Use Lambda + API Gateway + S3
- **Google Cloud**: Use Cloud Run
- **Azure**: Use App Service

## Monitoring & Logging

### Basic Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

### Metrics to Track
- API response times
- Error rates by module
- File upload sizes
- AI routing accuracy
- Database query times

## Future Enhancements

1. **User Authentication**
   - JWT-based auth
   - User accounts & data isolation

2. **Advanced Features**
   - Machine learning predictions
   - Real-time collaboration
   - Scheduling/automation
   - Custom workflows

3. **Performance**
   - Caching layer (Redis)
   - Async processing (Celery)
   - Background jobs

4. **Integrations**
   - More LLM providers
   - Salesforce, HubSpot
   - Power BI, Tableau
   - Slack notifications

5. **Scalability**
   - PostgreSQL backend
   - Microservices architecture
   - Kubernetes deployment
   - CDN for static files
