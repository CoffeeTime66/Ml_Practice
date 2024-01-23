from models.predictions import PredictRow
from utils.database import session_commit, get_session
from utils.tasks import process_response


def get_predict_rows_by_user(user_id, session=get_session()):
    return session.query(PredictRow).filter_by(User_id=user_id).all()


def add_predict_row(
        user_id,
        model,
        age_group,
        gender,
        sport_days,
        bmi,
        glucose,
        diabetes_degree,
        hemoglobin,
        insulin,
        result,
        session=get_session(),
):
    new_predict_row = PredictRow(
        User_id=user_id,
        model=model,
        age_group=age_group,
        gender=gender,
        sport_days=sport_days,
        bmi=bmi,
        glucose=glucose,
        diabetes_degree=diabetes_degree,
        hemoglobin=hemoglobin,
        insulin=insulin,
        result=result,
    )
    session.add(new_predict_row)
    session_commit(session)
    return new_predict_row


def predict(
        user_id,
        model,
        age,
        gender,
        sport_days,
        bmi,
        glucose,
        diabetes_degree,
        hemoglobin,
        insulin,
):
    data = {
        "user_id": user_id,
        "model": model,
        "age_group": age,
        "RIAGENDR": gender,
        "PAQ605": sport_days,
        "BMXBMI": bmi,
        "LBXGLU": glucose,
        "DIQ010": diabetes_degree,
        "LBXGLT": hemoglobin,
        "LBXIN": insulin,
    }
    process_response.delay(data)
