CREATE DATABASE IF NOT EXISTS test;
USE test;

CREATE TABLE person (id int, first_name varchar(255), last_name varchar(255));

INSERT INTO person VALUES
(1, 'Ones', 'Tamba'),
(2, 'Bambang', 'Sudibyo'),
(3, 'Joko', 'Marpaung');