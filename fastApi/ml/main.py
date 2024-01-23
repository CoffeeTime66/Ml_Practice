from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from joblib import load


app = FastAPI()


models = {
    0: load("models/linear.joblib"),
    1: load("models/gboost.joblib"),
    2: load("models/catboost.joblib"),
}


class InputData(BaseModel):
    user_id: int
    model: int
    age_group: int  # 0 for <65 or 1 for >=65
    RIAGENDR: float  # 0 for man or 1 for woman
    PAQ605: float  
    BMXBMI: float  
    LBXGLU: float  
    DIQ010: float  
    LBXGLT: float  
    LBXIN: float 


@app.post("/predict")
def predict(data: InputData):
    try:
        result = models[data.model].predict([[
                    data.age_group,
                    data.RIAGENDR,
                    data.PAQ605,
                    data.BMXBMI,
                    data.LBXGLU,
                    data.DIQ010,
                    data.LBXGLT,
                    data.LBXIN,]])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    return {
        "prediction": result.tolist(),
        }