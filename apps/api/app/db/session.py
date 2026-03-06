from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.settings import settings


engine = create_engine(
    settings.sqlalchemy_database_uri,
    echo=settings.echo,
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
