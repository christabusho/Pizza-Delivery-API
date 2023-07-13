from sqlalchemy.orm import declarative_base,sessionmaker 
from sqlalchemy import create_engine


engine=create_engine('postgresql://christadushime:christa07@localhost:5432/postgres',
    echo=True
)

Base=declarative_base()

Session=sessionmaker()


