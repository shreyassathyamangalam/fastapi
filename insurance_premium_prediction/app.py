# import necessary libraries

from fastapi.responses import JSONResponse
from fastapi import FastAPI
from schema.user_input import UserInput
from model.predict import predict_output, model_version, model
from schema.prediction_response import PredictionResponse

# Create the FastAPI app
app = FastAPI()

# Define the home endpoint
@app.get("/")
def home():
    return JSONResponse(status_code=200, content={"message": "Welcome to the Insurance Premium Prediction API!"})

# Define the health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "The API is running smoothly.",
        "model_version": model_version,
        "model_loaded": model is not None
    }


# Define the prediction endpoint
@app.post("/predict", response_model=PredictionResponse,
            responses={200: {"description": "Prediction successful"},
                       500: {"description": "Internal Server Error"}})
def predict_premium(data: UserInput):
    
    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }
    
    try:
    
        prediction = predict_output(user_input)
    
        return JSONResponse(status_code=200, content={'response': prediction})
    
    except Exception as e:
        
        return JSONResponse(status_code=500, content={'error': str(e)})
    
    
