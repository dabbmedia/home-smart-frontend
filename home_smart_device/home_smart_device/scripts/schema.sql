-- select database
-- \c home_smart_device;

-- CREATE ROLE home_smart_device LOGIN;
-- or
CREATE USER home_smart_device WITH PASSWORD 'home_smart_device';

CREATE DATABASE home_smart_device encoding UTF8 LC_COLLATE 'en_US.utf8' LC_CTYPE 'en_US.utf8' OWNER home_smart_device template template0;
CREATE SCHEMA home_smart_device;

GRANT CONNECT ON DATABASE home_smart_device TO home_smart_device;
GRANT USAGE ON SCHEMA public TO home_smart_device;


-- DROP TABLE network;
-- DROP TABLE actuator_event;
-- DROP TABLE actuator;
-- DROP TABLE sensor_event;
-- DROP TABLE sensor;
-- DROP TABLE device;
-- DROP TABLE room;
-- DROP TABLE floor;
-- DROP TABLE location;

CREATE TABLE location (
  id BIGSERIAL PRIMARY KEY,
  name text NOT NULL,
  description text,
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO location (name, description) VALUES ('Home', 'The main location.');

CREATE TABLE floor (
  id BIGSERIAL PRIMARY KEY,
  location_id BIGSERIAL NOT NULL REFERENCES location(id),
  name text NOT NULL,
  description text,
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO floor (location_id, name, description) VALUES (1, 'Ground', 'The main floor of this location.');
INSERT INTO floor (location_id, name, description) VALUES (1, 'Crawl Space', 'Dirt floor area below house.');

CREATE TABLE room (
  id BIGSERIAL PRIMARY KEY,
  floor_id BIGSERIAL NOT NULL REFERENCES floor(id),
  name text NOT NULL,
  description text,
  width numeric(4),
  length numeric(4),
  height numeric(4),
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO room (id, floor_id, name, description) VALUES (1, 1, 'Living Room', 'The main room.');
INSERT INTO room (id, floor_id, name, description) VALUES (2, 1, 'Office', 'The office.');
INSERT INTO room (id, floor_id, name, description) VALUES (3, 1, 'Dining Room', 'The dining and den area.');

CREATE TABLE device (
  id BIGSERIAL PRIMARY KEY,
  room_id BIGSERIAL NOT NULL REFERENCES room(id),
  name text NOT NULL,
  description text NULL,
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE device ADD COLUMN address inet;

INSERT INTO device (id, room_id, name, description) VALUES (1, 1, 'Raspberry Pi 4', 'Connected to TV.', '127.0.0.1');
INSERT INTO device (id, room_id, name, description) VALUES (2, 1, 'Raspberry Pi Zero', 'In 3D printed case.', '10.0.0.100');
INSERT INTO device (id, room_id, name, description) VALUES (3, 2, 'Raspberry Pi 2', 'On keyboard.', '10.0.0.102');
INSERT INTO device (id, room_id, name, description) VALUES (4, 3, 'Raspberry Pi 3', 'In window.', '10.0.0.103');

CREATE TYPE sensor_type AS ENUM ('video', 'audio', 'data');

CREATE TABLE sensor (
  id BIGSERIAL PRIMARY KEY,
  device_id BIGSERIAL NOT NULL REFERENCES device(id),
  type sensor_type,
  name text NOT NULL,
  description text NULL,
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO sensor (device_id, type, name, description) VALUES (1, 'video', 'Old Logitech USB', 'Old Logitech USB');
INSERT INTO sensor (device_id, type, name, description) VALUES (1, 'video', 'Internal Pi Cam', 'Internal Pi Cam');
INSERT INTO sensor (device_id, type, name, description) VALUES (2, 'video', 'PS2 USB Cam', 'PS2 USB Cam');
INSERT INTO sensor (device_id, type, name, description) VALUES (3, 'video', 'PS2 USB Cam', 'PS2 USB Cam');

CREATE TABLE sensor_event (
  id BIGSERIAL PRIMARY KEY,
  sensor_id BIGSERIAL NOT NULL REFERENCES sensor(id),
  name text NOT NULL,
  description text NULL,
  data jsonb NOT NULL,
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE actuator (
  id BIGSERIAL PRIMARY KEY,
  device_id BIGSERIAL NOT NULL REFERENCES device(id),
  name text NOT NULL,
  description text NULL,
  action_url text NULL,
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE actuator_event (
  id BIGSERIAL PRIMARY KEY,
  actuator_id BIGSERIAL NOT NULL REFERENCES actuator(id),
  name text NOT NULL,
  description text NULL,
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE network (
  id BIGSERIAL PRIMARY KEY,
  location_id BIGSERIAL NOT NULL REFERENCES location(id),
  name text NOT NULL,
  description text NULL,
  public_address inet NOT NULL,
  gateway_address inet NOT NULL,
  subnet_address inet NOT NULL,
  created timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO home_smart_device;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO home_smart_device;

-- SELECT 
--   l.id AS location_id, l.name AS location_name, l.description AS location_description, l.created AS location_created, 
--   f.id AS floor_id, f.name AS floor_name, 
--   r.id AS room_id, r.name AS room_name, 
--   d.id AS device_id, d.name AS device_name 
--   FROM location l 
--   LEFT JOIN floor f ON l.id = f.location_id 
--   LEFT JOIN room r ON f.id = r.floor_id 
--   LEFT JOIN device d ON r.id = d.room_id 
--   WHERE l.id = 1 
--   ORDER BY l.name, f.name, r.name, d.name ASC;

-- SELECT 
--   l.id AS location_id, 
--   l.name AS location_name, 
--   (SELECT ARRAY (
--     SELECT f.id AS floor_id, f.name AS floor_name, (SELECT ARRAY (
--           SELECT r.id AS room_id, r.name AS room_name 
--           FROM room r WHERE f.id = r.floor_id
--         ) AS rooms) 
--     FROM floor f WHERE l.id = f.location_id
--   ) AS floors)  
--   FROM location l
--   WHERE l.id = 1
--   ORDER BY l.name ASC;

-- db_cur.execute(
--         'SELECT '
--           'json_build_object( '
--             '\'location_id\', COALESCE(l.id, 0), '
--             '\'location_name\', COALESCE(l.name, \'\'), '
--             '\'location_created\', COALESCE(l.created, \'1999-01-01 00:00:00+00\'), '
--             '\'floors\', json_build_object( '
--               '\'floor_id\', COALESCE(f.id, 0), '
--               '\'floor_name\', COALESCE(f.name, \'\'), '
--               '\'rooms\', json_build_object( '
--                 '\'room_id\', COALESCE(r.id, 0), '
--                 '\'room_name\', COALESCE(r.name, \'\'), '
--                 '\'devices\', json_build_object( '
--                   '\'device_id\', COALESCE(d.id, 0), '
--                   '\'device_name\', COALESCE(d.name, \'\') '
--                 ') '
--               ') '
--             ') '
--           ') AS text '
--           'FROM location l '
--           'LEFT JOIN floor f ON l.id = f.location_id '
--           'LEFT JOIN room r ON f.id = r.floor_id '
--           'LEFT JOIN device d ON r.id = d.room_id '
--           'WHERE l.id = 1 '
--           'ORDER BY f.id ASC',
--         (id,)
--     )

-- SELECT 
--   l.id AS id,
--   l.name AS name,
--   l.created AS created,
--   ARRAY_AGG(
--     f.id AS id,
--     f.name AS name,
--     ARRAY_AGG(
--       r.id AS id,
--       r.name AS name,
--       ARRAY_AGG(
--         d.id AS id,
--         d.name AS name
--       ) AS devices
--     ) AS rooms
--   ) AS floors
--   FROM location l
--   LEFT JOIN floor f ON l.id = f.location_id
--   LEFT JOIN room r ON f.id = r.floor_id
--   LEFT JOIN device d ON r.id = d.room_id
--   WHERE l.id = 1
--   GROUP BY l.id, l.name, l.created
--   ORDER BY f.id ASC;
