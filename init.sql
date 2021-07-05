CREATE TABLE IF NOT EXISTS events (
  event_id INT NOT NULL,
  medication_name varchar(250) NOT NULL,
  action_name varchar(250) NOT NULL,
  event_time TIMESTAMP,
  status varchar(250) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  PRIMARY KEY (event_id)
);
