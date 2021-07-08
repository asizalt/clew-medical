import datetime
import os
import asyncpg
import dateutil

async def mock():
    conn = await asyncpg.connect(
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD'),
        database=os.environ.get('POSTGRES_DB'),
        host=os.environ.get('POSTGRES_HOST')
    )

    try:
        await conn.execute('''
                           INSERT INTO events(p_id, medication_name,start,stop) VALUES($1, $2, $3, $4)
                       ''', 3, 'Z', datetime.datetime(2020, 1, 31, 13, 14, 31),datetime.datetime(2020, 1, 31, 13, 20, 31))

    except Exception as e:
        pass
    conn.close()

