import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text

print(sqlalchemy.__version__)

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True) 

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

    conn.commit() 