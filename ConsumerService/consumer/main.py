import asyncio
from aiohttp import web
from routes import setup_routes
import os
from validation import process_message
import asyncpg
from aio_pika import connect, ExchangeType, Message, DeliveryMode, IncomingMessage
import logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


async def main(app):
    # web.run_app(init_app())
    db_connection = await db_connect()
    channel, queue_connection = await setup_rabbitmq()
    await parse_messages(channel,queue_connection,db_connection)


async def db_connect():
    conn = await asyncpg.connect(
                                user=os.environ.get('POSTGRES_USER'),
                                password=os.environ.get('POSTGRES_PASSWORD'),
                                database=os.environ.get('POSTGRES_DB'),
                                host=os.environ.get('POSTGRES_HOST')
                                )
    return conn


async def setup_rabbitmq():
    connection = await connect(host=os.environ.get('RABBIT_HOST'),
                               login=os.environ.get('RABBIT_USER'),
                               password=os.environ.get('RABBIT_PASS'),
                               # loop=loop
                               )
    # Creating a channel
    channel = await connection.channel()
    exchange = await channel.declare_exchange(
        "meds", ExchangeType.FANOUT
    )

    return channel, connection


    # await queue.basic_consume(queue='events', on_message_callback=callback, auto_ack=True)
    # return connection, exchange
async def parse_messages(channel,queue_connection,db_connection):
    queue = await channel.declare_queue(name='events', auto_delete=True)
    # await queue.consume(on_message, no_ack=True)
    async with queue.iterator() as queue_iter:
        # Cancel consuming after __aexit__
        async for message in queue_iter:
            async with message.process():
                # print(message.body.decode())
               await process_message(db_connection,message)

               if queue.name in message.body.decode():
                    break


async def start_background_tasks(app):
    app['rmq_listener'] = asyncio.create_task(main(app))
    app['pool'] = await asyncpg.create_pool(user=os.environ.get('POSTGRES_USER'),
                                            password=os.environ.get('POSTGRES_PASSWORD'),
                                            database=os.environ.get('POSTGRES_DB'),
                                             host=os.environ.get('POSTGRES_HOST')
                                            )
    # app.router.add_get("/", handle)
    setup_routes(app)
    # for route in routes.routes:
    #     app.router.add_route(*route)


     # return web.json_response({'id':'asi'},dumps=pretty_json,)

if __name__ == '__main__':
    logging.error("main has started")
    app = web.Application()
    logging.error("web has started")
    app.on_startup.append(start_background_tasks)
    web.run_app(app)

