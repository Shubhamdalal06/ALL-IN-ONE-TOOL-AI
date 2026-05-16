# AI All-in-One Data Tool

A powerful AI-driven data analysis platform that combines Excel operations, SQL queries, Six Sigma analysis, data cleaning, and Google Sheets integration in one unified tool.

## Features

### 🎯 Core Modules

1. **Excel Module** - Pivot tables, formulas, summaries, formatting
2. **SQL Module** - Query, filter, join, and aggregate data
3. **Six Sigma Module** - Pareto analysis, control charts, capability analysis
4. **Cleaning Module** - Remove duplicates, handle missing values, normalize data
5. **Google Sheets Module** - Read/write/sync with Google Sheets
6. **AI Router** - Claude-powered command interpretation and routing

### 🚀 Key Features

- Upload Excel, CSV, or JSON files
- Natural language commands for data operations
- AI-powered task routing to the right module
- Real-time data processing
- Download processed data as Excel files
- Quality reports and insights

## Architecture

```
AI All-in-One Tool/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── ai_router.py         # AI-powered command router
│   ├── requirements.txt      # Python dependencies
│   └── modules/
│       ├── file_loader.py    # File I/O operations
│       ├── excel_module.py   # Excel operations
│       ├── sql_module.py     # SQL queries
│       ├── sheets_module.py  # Google Sheets API
│       ├── sixsigma_module.py # Quality analysis
│       └── cleaning_module.py # Data cleaning
├── frontend/
│   └── index.html           # Web interface
├── data/                    # Output data folder
└── .env.example             # Environment variables template
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- pip or conda

### 1. Clone/Setup the Project

```bash
cd "AI All in One tool"
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate      # On macOS/Linux
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp ../.env.example ../.env
# Edit .env and add your API keys:
# - ANTHROPIC_API_KEY
# - GOOGLE_SHEETS_CREDENTIALS_PATH (optional)
```

### 5. Run the Backend

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 6. Open Frontend

Open `frontend/index.html` in your browser or serve it with a local server:

```bash
# Using Python
cd frontend
python -m http.server 8001
# Then visit http://localhost:8001
```

## API Endpoints

### File Operations
- `POST /upload` - Upload a data file
- `POST /download` - Download processed file

### Processing
- `POST /process` - Process data with AI routing

### Excel Operations
- `POST /excel/pivot` - Create pivot table
- `POST /excel/summary` - Get summary statistics

### Data Cleaning
- `POST /cleaning/remove-duplicates` - Remove duplicates
- `POST /cleaning/handle-missing` - Handle missing values

### Six Sigma Analysis
- `POST /sixsigma/pareto` - Pareto analysis
- `POST /sixsigma/control-chart` - Control chart analysis

## Usage Examples

### Example 1: Create a Pivot Table
1. Upload an Excel file
2. Command: "Create a pivot table by Department showing average Salary"
3. AI router identifies this as Excel module
4. Backend creates pivot table and returns results

### Example 2: Data Cleaning
1. Upload CSV with missing values
2. Command: "Remove duplicate rows and handle missing values"
3. AI router identifies this as Cleaning module
4. Backend processes data and returns cleaned dataset

### Example 3: Six Sigma Analysis
1. Upload quality data
2. Command: "Run Pareto analysis on defect types"
3. Backend identifies vital few defects causing 80% of issues

## AI Routing Logic

The system uses Claude to interpret user commands:

- **"chart", "pivot", "formula"** → Excel Module
- **"query", "filter", "join"** → SQL Module
- **"clean", "duplicate", "missing"** → Cleaning Module
- **"pareto", "control", "capability"** → Six Sigma Module
- **"sheets", "google", "sync"** → Sheets Module

## Configuration

### Database
- Default: SQLite (file-based at `./data/ai_tool.db`)
- Can be changed to PostgreSQL

### LLM API
- Default: Anthropic Claude 3.5 Sonnet
- Set `ANTHROPIC_API_KEY` in `.env`

## Troubleshooting

### API Connection Issues
- Ensure backend is running: `python main.py`
- Check port 8000 is available
- Verify CORS is enabled

### File Upload Errors
- Ensure file is Excel, CSV, or JSON
- Check file is not corrupted
- Verify sufficient disk space

### AI Router Issues
- Check `ANTHROPIC_API_KEY` is set
- Verify API key has proper permissions
- Check internet connection

## Future Enhancements

- [ ] Database backend for persistent storage
- [ ] User authentication and authorization
- [ ] Advanced visualization dashboard
- [ ] Real-time collaboration
- [ ] Mobile app support
- [ ] More LLM options (GPT-4, Gemini, etc.)
- [ ] Custom module creation
- [ ] Scheduled automation

## License

MIT

## Support

For issues or questions, please create an issue in the repository.
