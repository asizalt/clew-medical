import asyncio
import asyncpg
from aiohttp import web
from utils import pretty_json
import json
from datetime import date
import datetime
from json import JSONEncoder

def defaultconverter(o):
  if isinstance(o, datetime.datetime):
      return o.__str__()

async def all_events(request):
    """Handle incoming requests."""
    try:
        pool = request.app['pool']
        async with pool.acquire() as connection:
            # Open a transaction.
            async with connection.transaction():
                # Run the query passing the request argument.
                rows = await connection.fetch('SELECT * from events')
                print(rows)
                # result = dict(data)
                data = [dict(row) for row in rows]
        return web.json_response(data, dumps=pretty_json, )
    except Exception as e:
     print(e)

async def event_by_patient(request):
    patient_id = request.match_info['id']
    try:
        pool = request.app['pool']
        async with pool.acquire() as connection:
            # Open a transaction.
            async with connection.transaction():
                # Run the query passing the request argument.
                rows = await connection.fetch('SELECT * from events WHERE p_id=$1',int(patient_id))
                print(rows)
                # result = dict(data)
                data = [dict(row) for row in rows]
        return web.json_response(data, dumps=pretty_json, )
    except Exception as e:
        print(e)

