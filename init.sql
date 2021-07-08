CREATE TABLE IF NOT EXISTS events (
  event_id SERIAL ,
  p_id INT NOT NULL,
--  event_id INT NOT NULL,
  medication_name varchar(250) NOT NULL,
--  action varchar(250) NOT NULL,
--  event_time TIMESTAMP,
  start TIMESTAMP,
  stop TIMESTAMP,
  cancel_start TIMESTAMP,
  cancel_stop TIMESTAMP,
  status varchar(250) NOT NULL DEFAULT 'complete',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (p_id, medication_name)
--  PRIMARY KEY (event_id)
);
