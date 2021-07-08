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

async def events(request):
    """Handle incoming requests."""
    try:
        pool = request.app['pool']
        async with pool.acquire() as connection:
            # Open a transaction.
            async with connection.transaction():
                # Run the query passing the request argument.
                rows = await connection.fetch('SELECT p_id,medication_name,start,stop from events')
                # result = dict(data)
                data = [dict(row) for row in rows]
                if not data:
                    return web.json_response(data, status=404, dumps=pretty_json)
        return web.json_response(data, dumps=pretty_json, )
    except Exception as e:
     print(e)
     pass

async def event_by_patient(request):
    patient_id = request.match_info['id']
    try:
        pool = request.app['pool']
        async with pool.acquire() as connection:
            # Open a transaction.
            async with connection.transaction():
                # Run the query passing the request argument.
                rows = await connection.fetch('SELECT p_id,medication_name,start,stop from events WHERE p_id=$1',int(patient_id))
                # result = dict(data)
                data = [dict(row) for row in rows]
                if not data:
                    return web.json_response(data, status=404,dumps=pretty_json )
        return web.json_response(data, dumps=pretty_json, )
    except Exception as e:
        print(e)
        pass

async def event_patient_medication(request):
    patient_id = request.match_info['patient_id']
    medication_name = request.match_info['medication_id']
    try:
        pool = request.app['pool']
        async with pool.acquire() as connection:
            # Open a transaction.
            async with connection.transaction():
                # Run the query passing the request argument.
                rows = await connection.fetch('SELECT p_id,medication_name,start,stop'
                                              ' from events WHERE p_id=$1 AND medication_name=$2'
                ,int(patient_id),medication_name)
                # result = dict(data)
                data = [dict(row) for row in rows]
                if not data:
                    return web.json_response(data, status=404,dumps=pretty_json )
        return web.json_response(data, dumps=pretty_json, )
    except Exception as e:
        print(e)
        pass
