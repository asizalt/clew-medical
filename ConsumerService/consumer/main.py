import asyncio
import os
import ast
from dateutil import parser
import asyncpg
import logging    # first of all import the module
from aio_pika import connect, ExchangeType, Message, DeliveryMode, IncomingMessage

logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This message will get logged on to a file')

# async def on_message(message: IncomingMessage):
#     """
#     on_message doesn't necessarily have to be defined as async.
#     Here it is to show that it's possible.
#     """
#     print(" [x] Received message %r" % message)
#     print("Message body is: %r" % message.body)
#     print("Before sleep!")
#     await asyncio.sleep(1)  # Represents async I/O operations
#     print("After sleep!")

async def main(loop):
    db_connection = await db_connect()
    channel, queue_connection = await setup_rabbitmq(loop)
    await parse_messages(channel,queue_connection,db_connection)

async def db_connect():
    conn = await asyncpg.connect(
                                user='admin',
                                password='password',
                                database='clew_medical',
                                host='postgresdb'
                                )
    return conn


async def setup_rabbitmq(loop):
    connection = await connect(host=os.environ.get('RABBIT_HOST'),
                               login=os.environ.get('RABBIT_USER'),
                               password=os.environ.get('RABBIT_PASS'),
                               loop=loop
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

async def process_message(db_connection,message):
    parsed_message = message.body.decode('UTF-8')
    my_data = ast.literal_eval(parsed_message)
    if 'p_id' in my_data.keys():
        print(my_data['p_id'])
        await asyncio.sleep(1)
        date = parser.parse(my_data['event_time'])
        date_new = date.replace(tzinfo=None)
        try:
            await db_connection.execute('''
                    INSERT INTO events(p_id, medication_name,action_name,event_time) VALUES($1, $2, $3, $4)
                ''',
                                        int(my_data['p_id']),
                                        my_data['medication_name'],
                                        my_data['action'],
                                        date_new)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.create_task(main(loop))
    connection = loop.run_until_complete(main(loop))
    loop.run_forever()

    # try:
    #     loop.run_forever()
    # finally:
    #     loop.run_until_complete(connection.close())
