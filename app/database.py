from sqlmodel import create_engine, Session , SQLModel

DATABASE_URL= "sqlite:///e_commerce.db"

engine = create_engine(DATABASE_URL, echo= True)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    """Provide a new database session for each request."""
    with Session(engine) as Depsession:
        yield Depsession
