# clew-medical
application-assignment, publisher and consumer services

## starting the service
`docker-compose up`

Then ssh to the container `docker exec -it <container id> bash` and run main.py 

## sample publisher input data
```json
  {
    "p_id": "1",
    "medication_name": "X",
    "action": "start",
    "event_time": "2021-01-01T00:00:00+0000"
  },
  {
    "p_id": "1",
    "medication_name": "X",
    "action": "stop",
    "event_time": "2021-01-01T01:00:00+0000"
  },
  ```
