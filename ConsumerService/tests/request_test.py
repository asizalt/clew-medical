import pytest
from aiohttp import web
from consumer.views import events,event_by_patient,event_patient_medication
import asyncpg
import os
import json
import datetime


"""Require running database server"""

@pytest.fixture
async def cli(loop, aiohttp_client):
    app = web.Application()
    app['pool'] =  await asyncpg.create_pool(user='admin',
                                            password='password',
                                            database='clew_medical',
                                            host='postgresdb'
                                            )
    pool = app['pool']
    async with pool.acquire() as connection:
        # Open a transaction.
        async with connection.transaction():
            try:
                await connection.execute('''
                                           INSERT INTO events(p_id, medication_name,start,stop) VALUES($1, $2, $3, $4)
                                       ''', 3, 'Z', datetime.datetime(2020, 1, 31, 13, 14, 31),
                                   datetime.datetime(2020, 1, 31, 13, 20, 31))
            except Exception as e:
                pass
    app.router.add_get('/api/events', events)
    app.router.add_get('/api/patient/{id}', event_by_patient, name='event_by_patient')
    app.router.add_get('/api/patient/{patient_id}/medication/{medication_id}', event_patient_medication, name='event_patient_medication')
    return await aiohttp_client(app)


async def test_route_not_found(cli):
    resp = await cli.get('/')
    assert resp.status == 404
    assert await resp.text() == '404: Not Found'

async def test_index_events(cli):
    resp = await cli.get('/api/events')
    assert resp.status == 200

async def test_event_patient(cli):
    resp = await cli.get('/api/patient/3')
    assert resp.status == 200
    data = await resp.json()
    expected = [{
        "p_id": 3,
        "medication_name": "Z",
        "start": "2020-01-31 13:14:31",
        "stop": "2020-01-31 13:20:31"
    }]
    assert data == expected

async def test_event_patient_not_found(cli):
    resp = await cli.get('/api/patient/0')
    assert resp.status == 404

async def test_medication_patient(cli):
    resp = await cli.get('/api/patient/3/medication/Z')
    assert resp.status == 200
    data = await resp.json()
    expected = [{
        "p_id": 3,
        "medication_name": "Z",
        "start": "2020-01-31 13:14:31",
        "stop": "2020-01-31 13:20:31"
    }]
    assert data == expected
