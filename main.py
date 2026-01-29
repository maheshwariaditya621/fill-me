from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import models, schemas, crud, database

# Create tables if they don't exist
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Fill Me - A Premium Form Developer",
    description="A high-performance and premium data collection platform.",
    version="1.0.0"
)

# CORS (Allow all for development flexibility)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve current directory for images/CSS/JS
app.mount("/static", StaticFiles(directory="."), name="static")

@app.post("/submit-response", response_model=schemas.SurveyResponseOut, status_code=status.HTTP_201_CREATED)
def submit_response(response: schemas.SurveyResponseCreate, db: Session = Depends(database.get_db)):
    """
    Submit a new survey response.
    Validates all inputs against the questionnaire schema.
    """
    try:
        return crud.create_survey_response(db=db, response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Admin Secret Key (Change this to something secure)
ADMIN_SECRET_KEY = "FillMe@Admin_2025"

@app.get("/responses", response_model=list[schemas.SurveyResponseOut])
def read_responses(key: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Get all responses (Admin use).
    Requires a valid secret key.
    """
    if key != ADMIN_SECRET_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return crud.get_responses(db, skip=skip, limit=limit)

@app.get("/export-excel")
def export_excel(key: str = None, db: Session = Depends(database.get_db)):
    """
    Export all data to an Excel file (.xlsx) for analysis.
    Requires a valid secret key.
    """
    if key != ADMIN_SECRET_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    responses = crud.get_all_responses_for_export(db)
    
    if not responses:
        raise HTTPException(status_code=404, detail="No responses found to export.")

    # Convert to standard dict list
    data = []
    for r in responses:
        data.append({
            "ID": r.id,
            "Submitted At": r.submitted_at,
            "Name": r.full_name,
            "Email": r.email,
            "Age Group": r.age_group,
            "Household Type": r.household_type,
            "Awareness": "Yes" if r.awareness else "No",
            "Platforms Used": ", ".join(r.platforms_used) if r.platforms_used else "",
            "Other Platform Name": r.other_platform_name, # New column
            "Most Used Platform": r.most_used_platform,
            "Usage Frequency": r.usage_frequency,
            "Avg Order Value": r.average_order_value,
            "Time Saved": r.time_saved,
            "Categories": ", ".join(r.product_categories) if r.product_categories else "",
            "Purchase Freq Change": r.purchase_frequency_change,
            "Impulse Buying": r.impulse_buying,
            "Price Sensitivity": r.price_sensitivity,
            "Price Comparison": r.price_comparison,
            "Local Shop Impact": r.local_shops_impact,
            "Imp Delivery": r.importance_delivery,
            "Imp Convenience": r.importance_convenience,
            "Imp Pricing": r.importance_pricing,
            "Imp Availability": r.importance_availability,
            "Satisfaction": r.overall_satisfaction,
            "Future Intent": r.future_usage_intent,
            "Qualitative": r.qualitative_response
        })

    df = pd.DataFrame(data)
    
    # Create valid Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Survey Responses")
    
    output.seek(0)
    
    headers = {
        'Content-Disposition': 'attachment; filename="survey_responses.xlsx"'
    }
    return StreamingResponse(output, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.get("/")
@app.get("/index.html")
def root():
    # Return index.html from the root folder
    return FileResponse('index.html')

@app.get("/favicon.ico")
def favicon():
    # Quietly return empty 204 to stop favicon 404 logs
    from fastapi.responses import Response
    return Response(status_code=204)
