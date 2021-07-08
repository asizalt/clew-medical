import logging
from dateutil import parser
import ast
import asyncio

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

async def logging_error(error,my_data):
    print(5)
    logging.error("%s: Type %s for medication %s patient %s: ",
                  error,
                  my_data['action'],
                  my_data['medication_name'],
                  my_data['p_id'])

async def validate_input(my_data):
    print(4)
    if {'p_id', 'medication_name', 'event_time', 'action'} <= my_data.keys():
        if(my_data['p_id'].isdigit() == False or isinstance(my_data['p_id'], str) == False):
            print("Invalid Input type")
            logging.error("Invalid Input type")
            return False
        else:
            try:
                date = parser.parse(my_data['event_time'])
                date_new = date.replace(tzinfo=None)
            except ValueError:
                print("Invalid Date")
                logging.error("Invalid Date type for patient $s",my_data['patient'])
                pass;
        return True
    else:
        print("Invalid Action: Type")
        logging.error("Invalid Action: Type")
        return False
# can also be done with ON CONFLICT from postgres
async def process_message(db_connection,message):
    print(1)
    print(message.body.decode('UTF-8'))
    parsed_message = message.body.decode('UTF-8')
    my_data = ast.literal_eval(parsed_message)
    row = None
    await asyncio.sleep(1)
    is_valid = await validate_input(my_data)
    if is_valid == True:
        try:
            row =  await  db_connection.fetchrow(
                'SELECT * FROM events WHERE p_id = $1 AND medication_name=$2',int(my_data['p_id']),my_data['medication_name']
            )
            print(row, type(row))
        except Exception as e:
          print("I have an exception")
          print(e)

        if row is None:
            await insert_first_medication(db_connection,my_data)
        else:
            await validate_medication(db_connection,dict(row),my_data)
        print('I am here ')


async def insert_first_medication(db_connection,my_data):
    print(2)
    if my_data['action'] == 'start':
                date = parser.parse(my_data['event_time'])
                date_new = date.replace(tzinfo=None)
                try:
                    await db_connection.execute('''
                        INSERT INTO events(p_id, medication_name,start) VALUES($1, $2, $3)
                    ''',int(my_data['p_id']),my_data['medication_name'],date_new)

                except Exception as e:
                  print(e)


async def validate_medication(db_connection, row,my_data):
    # can also be done with ON CONFLICT from postgres
    date = parser.parse(my_data['event_time'])
    date_new = date.replace(tzinfo=None)
    my_data['event_time'] = date_new

    if (row[my_data['action']] != None):
        await logging_error('duplicate action',my_data)
    elif row['start'] != None and my_data['action'] == 'stop' and my_data['event_time'] <= row['start']:
        print(my_data['event_time'] )
        print(row['start'])
        await logging_error('Invalid start and stop time', my_data)
    else:
        try:
            #                await db_connection.execute('UPDATE events SET info=$2 WHERE id=$1', id_, new))
            if(my_data['action'] == 'stop'):
                await db_connection.execute('UPDATE events SET stop=$1 WHERE p_id=$2 AND medication_name=$3'
                                            , date_new, int(my_data['p_id']),my_data['medication_name'])
            elif(my_data['action'] == 'cancel_start'):
                await db_connection.execute('UPDATE events SET cancel_start=$1 WHERE p_id=$2 AND medication_name=$3'
                                            , date_new, int(my_data['p_id']), my_data['medication_name'])
            elif(my_data['action'] == 'cancel_stop'):
                await db_connection.execute('UPDATE events SET cancel_stop=$1 WHERE p_id=$2 AND medication_name=$3'
                                            , date_new, int(my_data['p_id']), my_data['medication_name'])
            else:
                pass
        except Exception as e:
            print(e)
            await logging_error('can not connect to DB please contact admin')
            pass

# async def logging_error(error,my_data):
#     print(5)
#     logging.error("$s: Type %s for medication $s patient $s: ",
#                   error,
#                   my_data['action'],
#                   my_data['medication_name'],
#                   my_data['p_id'])
