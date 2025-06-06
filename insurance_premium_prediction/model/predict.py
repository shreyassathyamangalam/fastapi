# Import necessary libraries
import pandas as pd
import pickle

# Load the pre-trained model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Model version
model_version = "1.0.0"

# Get the class labels from the model
class_labels = model.classes_.tolist()


# Define the prediction function
def predict_output(user_input: dict):
    """
    Predict the insurance premium category based on user input.
    
    Parameters:
    user_input (dict): A dictionary containing user input data.
    
    Returns:
    str: The predicted insurance premium category.
    """
    # Convert user input to DataFrame
    input_df = pd.DataFrame([user_input])
    
    # Make prediction
    predicted_class = model.predict(input_df)[0]
    
    # Get the probabilities for each class
    probabilities = model.predict_proba(input_df)[0]
    confidance = max(probabilities)
    
    # Create mapping of class labels to probabilities
    class_probs = dict(zip(class_labels, map(lambda x: round(x, 4), probabilities)))
    
    return {
        "predicted_category": predicted_class,
        "confidence": round(confidance, 4),
        "class_probabilities": class_probs
    }
