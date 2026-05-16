# Quick Start Guide

Get the AI All-in-One Tool running in 5 minutes!

## Step 1: Get Your API Key

1. Go to [Anthropic Console](https://console.anthropic.com)
2. Sign up or log in
3. Create an API key
4. Copy the key (you'll need this in Step 3)

## Step 2: Install Python

Make sure you have Python 3.8+ installed:

```bash
python --version
```

## Step 3: Setup the Project

### On Windows:
```bash
cd "AI All in One tool"
start_windows.bat
```

This will:
- Create virtual environment
- Install dependencies
- Start the backend server

### On macOS/Linux:
```bash
cd "AI All in One tool"
chmod +x start_unix.sh
./start_unix.sh
```

When prompted, paste your Anthropic API key into the `.env` file.

## Step 4: Open the Web Interface

1. Open `frontend/index.html` in your browser
2. Or serve it locally:
   ```bash
   cd frontend
   python -m http.server 8001
   ```
   Then visit: http://localhost:8001

## Step 5: Try It Out

### Example 1: Data Cleaning
1. Create a sample Excel file with some duplicate rows
2. Upload it
3. Command: "Remove duplicate rows"
4. See the cleaned data

### Example 2: Analysis
1. Upload a sales dataset
2. Command: "Create a pivot table by Region"
3. Get instant pivot table

### Example 3: Quality Analysis
1. Upload quality metrics
2. Command: "Run Pareto analysis"
3. See which 20% of causes drive 80% of issues

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r backend/requirements.txt
```

### "ANTHROPIC_API_KEY not found"
1. Edit `.env` file
2. Add: `ANTHROPIC_API_KEY=your_key_here`
3. Restart backend

### Frontend won't connect
- Check backend is running on http://localhost:8000
- Open browser DevTools (F12) to see error messages

### Port 8000 already in use
Edit `.env`:
```
SERVER_PORT=8001
```

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- Create custom modules for your specific needs
- Deploy to cloud (Heroku, AWS, GCP, etc.)

## Support

- Check backend logs in terminal
- Review API responses in browser Network tab
- Test endpoints with curl or Postman

```bash
# Test backend is running
curl http://localhost:8000

# Expected response: {"message": "AI All-in-One Tool API is running"}
```

Enjoy analyzing your data with AI! 🚀
