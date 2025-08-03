-- Michael Kosinski
-- Raul Gandara
-- Howard Rovira

DROP TABLE IF EXISTS apartment;
DROP TABLE IF EXISTS vacation_home;
DROP TABLE IF EXISTS land;
DROP TABLE IF EXISTS house;
DROP TABLE IF EXISTS neighborhood;
DROP TABLE IF EXISTS commercial;
DROP TABLE IF EXISTS rewards;
DROP TABLE IF EXISTS renter;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS card;
DROP TABLE IF EXISTS user_address;
DROP TABLE IF EXISTS property;
DROP TABLE IF EXISTS agent;
DROP TABLE IF EXISTS agency;
DROP TABLE IF EXISTS users;

CREATE TABLE users
(
	email		VARCHAR(50),
	first_name		VARCHAR(20),
	last_name		VARCHAR(20),
	PRIMARY KEY (email)
);

CREATE TABLE agency
(
	agency_name		VARCHAR(30),
	total_booking	NUMERIC(5,0),
	PRIMARY KEY (agency_name)
);

CREATE TABLE agent
(
	email		VARCHAR(50),
	job_title		VARCHAR(25),
	phone_number	VARCHAR(12),
	agency_name		VARCHAR(30),
	PRIMARY KEY (email),
	FOREIGN KEY (agency_name) REFERENCES agency,
	FOREIGN KEY (email) REFERENCES users
);

CREATE TABLE property
(
	id				VARCHAR(10),
	price			NUMERIC(6,2),
	sqft			NUMERIC(6,2),
	description		VARCHAR(250),
	street_addr		VARCHAR(50),
	city			VARCHAR(25),
	state			VARCHAR(20),
	zip				VARCHAR(5),
	agency_name		VARCHAR(30),
	rent_or_sale	VARCHAR(4) CHECK (rent_or_sale IN ('rent', 'sale')),
	move_in_date	NUMERIC(4,0),
	PRIMARY KEY (id),
	FOREIGN KEY (agency_name) REFERENCES agency
);

CREATE TABLE user_address
(
	email			VARCHAR(50),
	street_addr		VARCHAR(50),
	city			VARCHAR(25),
	state			VARCHAR(20),
	zip				VARCHAR(5),
	PRIMARY KEY (email, street_addr, city, state, zip),
	FOREIGN KEY (email) REFERENCES users
);

CREATE TABLE card
(
	number			VARCHAR(16),
	email			VARCHAR(50),
	name_on_card	VARCHAR(30),
	exp_date		VARCHAR(5),
	street_addr		VARCHAR(50),
	city			VARCHAR(25),
	state			VARCHAR(20),
	zip				VARCHAR(5),
	PRIMARY KEY (number),
	FOREIGN KEY (email) REFERENCES users,
	FOREIGN KEY (email, street_addr, city, state, zip) REFERENCES user_address
);

CREATE TABLE booking
(
    id SERIAL PRIMARY KEY,
    property_id VARCHAR(10) REFERENCES property(id),
    card_number VARCHAR(16) REFERENCES card(number),
    ini_time DATE,
    end_time DATE,
    status VARCHAR(15)
);

CREATE TABLE renter
(
	email		VARCHAR(50),
	move_in_date	NUMERIC(4,0),
	budget			NUMERIC(6,2),
	location		VARCHAR(100),
	number			VARCHAR(16),
	PRIMARY KEY (email),
	FOREIGN KEY (number) REFERENCES card,
	FOREIGN KEY (email) REFERENCES users
);

CREATE TABLE rewards
(
	email		VARCHAR(50),
	points			NUMERIC(6,0),
	PRIMARY KEY (email),
	FOREIGN KEY (email) REFERENCES users
);

CREATE TABLE commercial
(
	id							VARCHAR(10),
	commercial_building_type	VARCHAR(20),
	PRIMARY KEY (id),
	FOREIGN KEY (id) REFERENCES property
);

CREATE TABLE neighborhood
(
	neighborhood_name	VARCHAR(20),
	crime_rate		VARCHAR(4),
	nearby_schools	NUMERIC(2,0),
	PRIMARY KEY (neighborhood_name)
);

CREATE TABLE house
(
	id				VARCHAR(10),
	bedrooms		NUMERIC(2,0),
	neighborhood_name	VARCHAR(20),
	PRIMARY KEY (id),
	FOREIGN KEY (id) REFERENCES property,
	FOREIGN KEY (neighborhood_name) REFERENCES neighborhood
);

CREATE TABLE land
(
	id				VARCHAR(10),
	PRIMARY KEY (id),
	FOREIGN KEY (id) REFERENCES property
);

CREATE TABLE vacation_home
(
	id				VARCHAR(10),
	bedrooms		NUMERIC(2,0),
	PRIMARY KEY (id),
	FOREIGN KEY (id) REFERENCES property
);

CREATE TABLE apartment
(
	id					VARCHAR(10),
	bedrooms			NUMERIC(2,0),
	apt_building_type	VARCHAR(20),
	PRIMARY KEY (id),
	FOREIGN KEY (id) REFERENCES property
);
