from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):
    predicted_category: str = Field(..., description="The predicted category for the input data.")
    confidence: float = Field(..., description="The confidence level of the prediction, ranging from 0 to 1.", examples=[0.85])
    class_probabilities: Dict[str, float] = Field(
        ..., description="A dictionary containing the probabilities for each class.",
        examples=[{
            "Low": 0.05,
            "Medium": 0.10,
            "High": 0.85
        }]
    )
