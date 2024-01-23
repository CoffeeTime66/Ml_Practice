from fastapi import APIRouter, HTTPException, Request

from schemas.predictions import InputData
from utils.users import get_current_user, get_user_by_username, get_bill_by_user_id, update_bill
from utils.predictions import predict, get_predict_rows_by_user, \
                                    add_predict_row

router = APIRouter()

model_to_money = {0: 10, 1: 15, 2: 20}

@router.post("/add_row")
async def add_row(request: Request):
    json_body = await request.json()
    bill = get_bill_by_user_id(json_body["user_id"])
    cost = model_to_money[int(json_body["model"])]
    update_bill(bill.id, bill.money - cost)
    add_predict_row(
        user_id=json_body["user_id"],
        model=json_body["model"],
        age_group=json_body["age_group"],
        gender=json_body["RIAGENDR"],
        sport_days=json_body["PAQ605"],
        bmi=json_body["BMXBMI"],
        glucose=json_body["LBXGLU"],
        diabetes_degree=json_body["DIQ010"],
        hemoglobin=json_body["LBXGLT"],
        insulin=json_body["LBXIN"],
        result=json_body["result"],
    )
    
     
@router.post("/send_data")
async def send_data_for_processing(request: Request):
    json_body = await request.json()
    current_user = get_current_user(json_body["token"])
    user = get_user_by_username(current_user)
    if user:
        bill = get_bill_by_user_id(user.id)
        cost = model_to_money[int(json_body["model"])]
        if json_body["age_group"] == "yes":
            age_group = 1
        else: 
            age_group = 0
        if json_body["RIAGENDR"] == "male":
            gender = 0
        else:
            gender = 1      
        if (bill.money - cost) >= 0:
            predict(
                user.id,
                model=json_body["model"],
                age=age_group,
                gender=gender,
                sport_days=json_body["PAQ605"],
                bmi=json_body["BMXBMI"],
                glucose=json_body["LBXGLU"],
                diabetes_degree=json_body["DIQ010"],
                hemoglobin=json_body["LBXGLT"],
                insulin=json_body["LBXIN"],
            )
        else:
            return {"message": "Not enough units in account"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/user/predict_rows")
def get_user_predict_rows(request: Request):
    headers = request.headers
    current_user = get_current_user(headers["token"])
    user = get_user_by_username(current_user)
    if user:
        predict_rows = get_predict_rows_by_user(user.id)
        return {
            "user_id": user.id,
            "username": user.username,
            "predict_rows": predict_rows,
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
