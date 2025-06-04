import pickle
import pandas as pd
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

with open(MODEL_PATH,"rb") as f:
    model = pickle.load(f)

# MLFlow    

MODEL_VERSION = "1.0.0"

class_labels = model.classes_.tolist()

def predict_output(user_input: dict) -> dict:
    input_df = pd.DataFrame([{
        'bmi': user_input['bmi'],
        'lifestyle_risk': user_input['lifestyle_risk'],
        'age_group': user_input['age_group'],
        'city_tier': user_input['city_tier'],
        'occupation': user_input['occupation'],
        'income_lpa': user_input['income_lpa']
    }])

    prediction_class = model.predict(input_df)[0]

    # Get Probabilities for all classes
    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)

    class_probs = dict(zip(class_labels, map(lambda p:round(p,4),probabilities)))

    return {
        "predicted_category": prediction_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }