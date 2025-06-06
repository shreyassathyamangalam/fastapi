from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
from config.city_tier import tier_1_cities, tier_2_cities


# Define the pydantic data model to validate incoming data
class UserInput(BaseModel):
    age: Annotated[int, Field(..., title="Age", description="Age of the user", gt=0, le=120)]
    weight: Annotated[float, Field(..., title="Weight", description="Weight of the user in kg", gt=0)]
    height: Annotated[float, Field(..., title="Height", description="Height of the user in meters", gt=0, le=2.5)]
    income_lpa: Annotated[float, Field(..., title="Income", description="Annual income in lakhs per annum", gt=0)]
    smoker: Annotated[bool, Field(..., title="Smoker", description="Is the user a smoker?")]
    city: Annotated[str, Field(..., title="City", description="City of residence")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'], Field(title="Occupation", description="Occupation of the user")]
    
    # validate the city field
    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        v = v.strip().title()
        return v
    
    # Computed field for BMI
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
    
    # Computed field for lifestyle risk
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    # Computed field for age group
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age <= 25:
            return "young"
        elif 26 <= self.age <= 45:
            return "adult"
        elif 46 <= self.age <= 65:
            return "middle_aged"
        else:
            return "senior"
        
    # Computed filed for city tier
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3