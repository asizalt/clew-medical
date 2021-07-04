import asyncio
import os
import aio_pika
import time
import logging    # first of all import the module
from aio_pika import connect, ExchangeType, Message, DeliveryMode

logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This message will get logged on to a file')

async def main(loop):
    connection, exchange = await setup_rabbitmq(loop)

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
    queue = await channel.declare_queue(name='events', auto_delete=True)

    async with queue.iterator() as queue_iter:
        # Cancel consuming after __aexit__
        async for message in queue_iter:
            async with message.process():
                print(message.body)

                if queue.name in message.body.decode():
                    break

    
    # await queue.basic_consume(queue='events', on_message_callback=callback, auto_ack=True)
    # return connection, exchange


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main(loop))
    # try:
    #     loop.run_forever()
    # finally:
    #     loop.run_until_complete(connection.close())
