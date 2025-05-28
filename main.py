# imports
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

# define app
app = FastAPI()

# define the data model
class Patient(BaseModel):
    
    id: Annotated[str, Field(..., description="Unique identifier for the patient", examples=['P001'])]
    name: Annotated[str, Field(..., description="Name of the patient", examples=['John Doe'])]
    city: Annotated[str, Field(..., description="City where the patient resides", examples=['New York'])]
    age: Annotated[int, Field(..., gt=0, le=120, description="Age of the patient")]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in meters", examples=[1.75])]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kilograms", examples=[70.5])]
    
    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate Body Mass Index (BMI)"""
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        """Determine the health verdict based on BMI"""
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"
    

# define pydantic model to update patient data
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None, description="Name of the patient")]
    city: Annotated[Optional[str], Field(default=None, description="City where the patient resides")]
    age: Annotated[Optional[int], Field(default=None, gt=0, le=120, description="Age of the patient")]
    gender: Annotated[Optional[Literal['male', 'female', 'other']], Field(default=None, description="Gender of the patient")]
    height: Annotated[Optional[float], Field(default=None, gt=0, description="Height of the patient in meters")]
    weight: Annotated[Optional[float], Field(default=None, gt=0, description="Weight of the patient in kilograms")]
    


# function to load data from a file
def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

# function to save data to a file
def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)

# define a simple route
@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

# define another route
@app.get("/about")
def about():
    return {"message": "A fully functional Patient Management System API built with FastAPI."}

# define a route to view all patients data
@app.get("/view")
def view():
    data = load_data()
    return data

# defeine a route to view a specific patient data(path parameter)
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., title="The ID of the patient to view", description="This is the ID of the patient you want to view.", examples="P001")):
    # load data from the file
    data = load_data()
    # check if the patient_id exists in the data
    if patient_id in data:
        # return the patient data
        return data[patient_id]
    else:
        # return an error message
        raise HTTPException(status_code=404, detail="Patient not found")
    
# define a route to sort patients data(query parameter)
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., title="Sort by", description="The field to sort the patients by", example="height"), order: str = Query(title="Order", description="The order to sort the patients by", example="ascending", default="ascending")):
        
    valid_sort_fields = ["height", "weight", "bmi"]
        
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field, select from {valid_sort_fields}")
        
    if order not in ["ascending", "descending"]:
        raise HTTPException(status_code=400, detail=f"Invalid sort order, select from ['ascending', 'descending']")
        
    # load data from the file
    data = load_data()
        
    # sort the data
    sort_order = True if order == "ascending" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by), reverse=sort_order)
        
    # return the sorted data
    return sorted_data

# define a route to add a new patient
@app.post("/create")
def create_patient(patient: Patient):
    
    # load data from the file
    data = load_data()
    
    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    
    # add the new patient to the data
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    # save into the JSON file
    save_data(data)
    
    return JSONResponse(status_code=201, content={"message": "Patient created successfully", "patient": data[patient.id]})

    
# define a route to update a patient
@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    
    # load data from the file
    data = load_data()
    
    # check if patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # extract the existing patient data
    existing_patient_info = data[patient_id]
    
    # convert the update model to a dictionary
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    
    # update the existing patient data with the new values
    for key, value in updated_patient_info.items():
        if value is not None:
            existing_patient_info[key] = value
    
    # add "id" field to existing_patient_info, convert the exisintg_patient_info back to a Pydantic model, then update BMI and verdict, then convert it back to a dictionary
    existing_patient_info['id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info)
    existing_patient_info = patient_pydantic_object.model_dump(exclude='id')
    
    # save the updated data back to the file
    data[patient_id] = existing_patient_info
    
    # save into the JSON file
    save_data(data)
    
    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})

# define a route to delete a patient
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    
    # load data from the file
    data = load_data()
    
    # check if patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # delete the patient from the data
    del data[patient_id]
    
    # save into the JSON file
    save_data(data)
    
    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})

