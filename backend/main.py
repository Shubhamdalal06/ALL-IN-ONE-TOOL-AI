from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import pandas as pd
from typing import Optional
import io
from pathlib import Path

from modules.file_loader import FileLoader
from modules.excel_module import ExcelModule
from modules.sql_module import SQLModule
from modules.sheets_module import SheetsModule
from modules.sixsigma_module import SixSigmaModule
from modules.cleaning_module import CleaningModule
from ai_router import AIRouter

# Initialize FastAPI app
app = FastAPI(title="AI All-in-One Data Tool", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
file_loader = FileLoader()
excel_module = ExcelModule()
sql_module = SQLModule()
sheets_module = SheetsModule()
sixsigma_module = SixSigmaModule()
cleaning_module = CleaningModule()
ai_router = AIRouter()

# Store uploaded dataframes in memory (in production, use a database)
uploaded_data = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI All-in-One Tool API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a data file (Excel, CSV, JSON)
    """
    try:
        contents = await file.read()
        df, file_type = file_loader.load_from_bytes(contents, file.filename)
        
        # Store dataframe
        file_id = file.filename.replace('.', '_')
        uploaded_data[file_id] = df
        
        # Get dataframe info
        info = file_loader.get_dataframe_info(df)
        
        return {
            "success": True,
            "file_id": file_id,
            "filename": file.filename,
            "file_type": file_type,
            "info": info,
            "message": f"File uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading file: {str(e)}")

@app.post("/process")
async def process_data(
    file_id: str = Form(...),
    user_command: str = Form(...),
    module_hint: Optional[str] = Form(None)
):
    """
    Process user command with AI routing
    """
    try:
        if file_id not in uploaded_data:
            raise HTTPException(status_code=404, detail="File not found")
        
        df = uploaded_data[file_id]
        
        # Get dataframe info for AI context
        df_info = file_loader.get_dataframe_info(df)
        
        # Route command using AI
        routing = ai_router.interpret_command(user_command, df_info)
        
        # Execute based on routing
        result = execute_routing(df, routing)
        
        return {
            "success": True,
            "routing": routing,
            "result": result,
            "message": "Processing complete"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")

@app.post("/excel/pivot")
async def create_pivot(
    file_id: str = Form(...),
    index: str = Form(...),
    columns: Optional[str] = Form(None),
    values: Optional[str] = Form(None),
    aggfunc: str = Form("sum")
):
    """Create pivot table"""
    try:
        if file_id not in uploaded_data:
            raise HTTPException(status_code=404, detail="File not found")
        
        df = uploaded_data[file_id]
        pivot = excel_module.create_pivot_table(df, index, columns, values, aggfunc)
        
        return {
            "success": True,
            "data": pivot.to_dict(),
            "shape": pivot.shape
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/excel/summary")
async def get_summary(file_id: str = Form(...)):
    """Get summary statistics"""
    try:
        if file_id not in uploaded_data:
            raise HTTPException(status_code=404, detail="File not found")
        
        df = uploaded_data[file_id]
        summary = excel_module.create_summary(df)
        
        return {
            "success": True,
            "summary": summary.to_dict(),
            "quality": cleaning_module.get_quality_report(df)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/cleaning/remove-duplicates")
async def remove_duplicates(file_id: str = Form(...)):
    """Remove duplicate rows"""
    try:
        if file_id not in uploaded_data:
            raise HTTPException(status_code=404, detail="File not found")
        
        df = uploaded_data[file_id]
        df_clean, message = cleaning_module.remove_duplicates(df)
        uploaded_data[file_id] = df_clean
        
        return {
            "success": True,
            "message": message,
            "rows_remaining": len(df_clean)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/cleaning/handle-missing")
async def handle_missing(
    file_id: str = Form(...),
    strategy: str = Form("drop")
):
    """Handle missing values"""
    try:
        if file_id not in uploaded_data:
            raise HTTPException(status_code=404, detail="File not found")
        
        df = uploaded_data[file_id]
        df_clean, message = cleaning_module.handle_missing_values(df, strategy)
        uploaded_data[file_id] = df_clean
        
        return {
            "success": True,
            "message": message,
            "rows_remaining": len(df_clean)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/sixsigma/pareto")
async def pareto_analysis(
    file_id: str = Form(...),
    defect_column: str = Form(...),
    count_column: Optional[str] = Form(None)
):
    """Run Pareto analysis"""
    try:
        if file_id not in uploaded_data:
            raise HTTPException(status_code=404, detail="File not found")
        
        df = uploaded_data[file_id]
        result_df, insight = sixsigma_module.pareto_analysis(df, defect_column, count_column)
        
        return {
            "success": True,
            "data": result_df.to_dict(),
            "insight": insight
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/sixsigma/control-chart")
async def control_chart(
    file_id: str = Form(...),
    value_column: str = Form(...)
):
    """Analyze control chart"""
    try:
        if file_id not in uploaded_data:
            raise HTTPException(status_code=404, detail="File not found")
        
        df = uploaded_data[file_id]
        analysis = sixsigma_module.control_chart_analysis(df, value_column)
        
        return {
            "success": True,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/download")
async def download_file(
    file_id: str = Form(...),
    format: str = Form("excel")
):
    """Download processed data"""
    try:
        if file_id not in uploaded_data:
            raise HTTPException(status_code=404, detail="File not found")
        
        df = uploaded_data[file_id]
        
        # Create output file
        Path("./data").mkdir(exist_ok=True)
        output_path = f"./data/{file_id}_output.xlsx"
        
        excel_module.save_with_formatting(df, output_path, title="Processed Data")
        
        return FileResponse(
            path=output_path,
            filename=f"{file_id}_output.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def execute_routing(df: pd.DataFrame, routing: dict) -> dict:
    """Execute command based on AI routing"""
    module = routing.get("module", "").upper()
    
    if module == "EXCEL_MODULE":
        if routing.get("function") == "create_pivot_table":
            return {
                "type": "pivot_table",
                "data": excel_module.create_pivot_table(df, **routing.get("parameters", {})).to_dict()
            }
        elif routing.get("function") == "create_summary":
            return {
                "type": "summary",
                "data": excel_module.create_summary(df, **routing.get("parameters", {})).to_dict()
            }
    
    elif module == "CLEANING_MODULE":
        if routing.get("function") == "remove_duplicates":
            df_clean, msg = cleaning_module.remove_duplicates(df)
            return {"type": "cleaning", "message": msg, "rows": len(df_clean)}
        elif routing.get("function") == "handle_missing_values":
            df_clean, msg = cleaning_module.handle_missing_values(df, **routing.get("parameters", {}))
            return {"type": "cleaning", "message": msg, "rows": len(df_clean)}
    
    elif module == "SIXSIGMA_MODULE":
        if routing.get("function") == "pareto_analysis":
            result_df, insight = sixsigma_module.pareto_analysis(df, **routing.get("parameters", {}))
            return {"type": "pareto", "data": result_df.to_dict(), "insight": insight}
    
    return {"type": "unknown", "data": None}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVER_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
