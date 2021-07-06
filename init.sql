CREATE TABLE IF NOT EXISTS events (
  event_id SERIAL PRIMARY KEY,
  p_id INT NOT NULL,
--  event_id INT NOT NULL,
  medication_name varchar(250) NOT NULL,
  action_name varchar(250) NOT NULL,
  event_time TIMESTAMP,
  status varchar(250) NOT NULL DEFAULT 'complete',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
--  PRIMARY KEY (event_id)
);
