from sqlmodel import SQLModel , create_engine, Session

DATABASE_URL = "sqlite:///./kitaab.db"

engine = create_engine(DATABASE_URL, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)
    #engine will we conveting fun into sql query (self)

def get_session():
    with Session(engine) as session:
        yield session # to give acces only when indeed
