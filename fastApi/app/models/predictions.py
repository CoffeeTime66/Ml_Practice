from models.users import *
from models.database import engine


class PredictRow(Base):
    __tablename__ = "Predict_row"

    id = Column(Integer, primary_key=True, autoincrement=True)
    User_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    model = Column(Integer, nullable=False)
    age_group = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    sport_days = Column(Integer, nullable=False)
    bmi = Column(Float, nullable=False)
    glucose = Column(Float, nullable=False)
    diabetes_degree = Column(Float, nullable=False)
    hemoglobin = Column(Float, nullable=False)
    insulin = Column(Float, nullable=False)
    result = Column(Float, nullable=False)

    user = relationship("User", back_populates="predictions")


Base.metadata.create_all(bind=engine)
