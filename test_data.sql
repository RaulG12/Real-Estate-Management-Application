-- fill this in with some test tuples later

INSERT INTO users (email, first_name, last_name) VALUES
('mkosinski@hawk.iit.edu', 'Michael', 'Kosinski'),
('hrovira@hawk.iit.edu', 'Howard', 'Rovira'),
('rgandara@hawk.iit.edu', 'Raul', 'Gandara');

INSERT INTO rewards (email, points) VALUES
('rgandara@hawk.iit.edu', 3184);

INSERT INTO agency (agency_name, total_booking) VALUES
('Illinois Tech', 0);

INSERT INTO renter (email, move_in_date, budget, location) VALUES
('mkosinski@hawk.iit.edu', 2025, 5000, 'Albuquerque'),
('rgandara@hawk.iit.edu', 2025, 5000, 'Chicago'),
('hrovira@hawk.iit.edu', 2025, 5000, 'Chicago');

INSERT INTO agent (email, job_title, phone_number, agency_name) VALUES 
('mkosinski@hawk.iit.edu', 'Student', '123-456-7890', 'Illinois Tech'),
('rgandara@hawk.iit.edu', 'Student', '123-456-7890', 'Illinois Tech'),
('hrovira@hawk.iit.edu', 'Student', '123-456-7890', 'Illinois Tech');

INSERT INTO user_address (email, street_addr, city, state, zip) VALUES
('mkosinski@hawk.iit.edu', '742 Evergreen Terrace', 'Springfield', 'Illinois', '62704'),
('rgandara@hawk.iit.edu', '908 Pinewood Ave', 'Boulder', 'Colorado', '80302'),
('hrovira@hawk.iit.edu', '12 Harborview Drive', 'Seattle', 'Washington', '98101');

INSERT INTO card (number, email, name_on_card, exp_date, street_addr, city, state, zip) VALUES
('4539148803436467', 'mkosinski@hawk.iit.edu', 'Michael Kosinski', '08/27', '742 Evergreen Terrace', 'Springfield', 'Illinois', '62704'),
('6011789012345678', 'rgandara@hawk.iit.edu', 'Raul Gandara', '01/26', '908 Pinewood Ave', 'Boulder', 'Colorado', '80302'),
('3792822463240005', 'hrovira@hawk.iit.edu', 'Howard Rovira', '12/25', '12 Harborview Drive', 'Seattle', 'Washington', '98101');

INSERT INTO neighborhood (neighborhood_name, crime_rate, nearby_schools) VALUES
('Bronzeville', 'idk', '12');

INSERT INTO property (id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date) VALUES
(1, 4000, 2000, 'Rowe Village North -- the entire building', '3303 S State St', 'Chicago', 'Illinois', '60616', 'Illinois Tech', 'rent', '2025');
INSERT INTO house (id, bedrooms, neighborhood_name) VALUES
(1, 80, 'Bronzeville');

INSERT INTO property (id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date) VALUES
(2, 450, 100, 'Cunningham Hall Apartment', '3100 S Michigan Ave', 'Chicago', 'Illinois', '60616', 'Illinois Tech', 'rent', '2025');
INSERT INTO apartment (id, bedrooms, apt_building_type) VALUES
(2, 2, 'Double');

INSERT INTO property (id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date) VALUES
(3, 3000, 500, 'Walter Whites House', '308 Negra Arroyo Lane', 'Albuquerque', 'New Mexico', '87111', 'Illinois Tech', 'sale', '2025');
INSERT INTO vacation_home (id, bedrooms) VALUES
(3, 3);

INSERT INTO property (id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date) VALUES
(4, 2000, 800, 'Siegel Field', '3301 S Dearborn St', 'Chicago', 'Illinois', '60616', 'Illinois Tech', 'sale', '2025');
INSERT INTO land (id) VALUES
(4);

INSERT INTO property (id, price, sqft, description, street_addr, city, state, zip, agency_name, rent_or_sale, move_in_date) VALUES
(5, 600, 1500, 'The Commons', '3201 S State St', 'Chicago', 'Illinois', '60616', 'Illinois Tech', 'rent', '2025');
INSERT INTO commercial (id, commercial_building_type) VALUES
(5, 'Dining');

INSERT INTO booking(id, property_id, card_number, ini_time, end_time, status) VALUES
('1', '1', '6011789012345678', '2025-05-10', '2025-07-10', 'booked');