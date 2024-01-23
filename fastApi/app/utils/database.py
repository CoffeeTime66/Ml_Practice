from sqlalchemy.orm import sessionmaker


from models.database import create_engine, SQLALCHEMY_DATABASE_URL


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


def get_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def session_commit(session):
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise e