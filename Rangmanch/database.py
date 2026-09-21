from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///rangmanch.db"

engine = create_engine(DATABASE_URL, echo=True)

def create_tables():
    "Create all tables defined by SQLModel Class"
    SQLModel.metadata.create_all(engine)

def get_session():
    "Dependeny that provides a databases session per session"
    with Session(engine) as session:
        yield session


# comlete SQLModel connecting with the DB        