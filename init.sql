CREATE TABLE IF NOT EXISTS events (
  product_id INT NOT NULL,
  medication_name varchar(250) NOT NULL,
  action_name varchar(250) NOT NULL,
  event_time TIMESTAMP,
  status varchar(250) NOT NULL,
  updated_at DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  created_at DEFAULT CURRENT_TIMESTAMP
  PRIMARY KEY (product_id)
);
