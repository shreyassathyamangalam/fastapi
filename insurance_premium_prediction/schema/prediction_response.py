# Import necessary libraries
from pydantic import BaseModel, Field
from typing import Dict

# Define the PredictionResponse schema
class PredictionResponse(BaseModel):
    """
    Schema for the prediction response.
    
    Attributes:
        predicted_category (str): The predicted insurance premium category.
        confidence (float): The confidence level of the prediction.
        class_probabilities (Dict[str, float]): A dictionary mapping class labels to their probabilities.
    """
    predicted_category: str = Field(..., description="The predicted insurance premium category.", examples=["low", "medium", "high"])
    confidence: float = Field(..., description="The confidence level of the prediction (ranges from 0 to 1)")
    class_probabilities: Dict[str, float] = Field(..., description="A dictionary mapping class labels to their probabilities.")
    