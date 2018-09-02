CREATE DATABASE dalla_stats;

CREATE USER 'dalla'@'%'
  IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON dalla_stats.* TO 'dalla'@'%';

USE dalla_stats;

CREATE TABLE person (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255),
  password_salt VARCHAR(255),
  on_peak BIGINT,
  off_peak BIGINT,
  PRIMARY KEY (id)
);

INSERT INTO person (id, username, password_hash, password_salt, on_peak, off_peak)
  VALUES(1, 'Unknown', 'NO_LOGIN', 'NO_LOGIN', 0, 0);

CREATE TABLE device (
  id INT NOT NULL AUTO_INCREMENT,
  mac_address CHAR(17) NOT NULL UNIQUE ,
  person_id INT NOT NULL,
  total_bytes BIGINT,
  on_peak BIGINT,
  off_peak BIGINT,
  description VARCHAR(255),
  PRIMARY KEY (id),
  FOREIGN KEY (person_id) REFERENCES person(id)
);

CREATE TABLE history (
  id INT NOT NULL AUTO_INCREMENT,
  device_id INT NOT NULL,
  ip_address VARCHAR(15),
  record_time INT NOT NULL,
  total_bytes BIGINT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (device_id) REFERENCES device(id)
);