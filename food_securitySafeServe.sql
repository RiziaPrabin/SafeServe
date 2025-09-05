USE food_security_db;
-- Hotels Table
CREATE TABLE hotels (
    hotel_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    contact_number VARCHAR(20),
    email VARCHAR(255),
    license_number VARCHAR(50),
    rating DECIMAL(2, 1),
    last_inspection_date DATE,
    status ENUM('Active', 'Closed', 'Suspended')
);
-- Inspector Table
CREATE TABLE inspectors (
    inspector_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    contact_number VARCHAR(20),
    email VARCHAR(255),
    region_assigned VARCHAR(255),
    qualifications TEXT
);
-- Inspections Table
CREATE TABLE inspections (
    inspection_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT,
    inspection_date DATE,
    inspector_id INT,
    overall_result ENUM('Passed', 'Failed', 'Needs Improvement'),
    comments TEXT,
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id),
    FOREIGN KEY (inspector_id) REFERENCES inspectors(inspector_id)
);


-- Food Poisoning Cases Table
CREATE TABLE food_poisoning_cases (
    case_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT,
    report_date DATE,
    symptoms TEXT,
    number_of_people_affected INT,
    investigation_status TEXT,
    conclusion TEXT,
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
);
-- Customer Feedback Table
CREATE TABLE customer_feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT,
    feedback_date DATE,
    customer_name VARCHAR(255),
    feedback_content TEXT,
    action_taken TEXT,
    status TEXT,
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
);
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100),
    password VARCHAR(255) NOT NULL -- Store hashed passwords for security
    
);
show tables;
-- Add a password column to the inspectors table
ALTER TABLE inspectors
ADD COLUMN password VARCHAR(255) NOT NULL;

-- Create a new table for hotel managers
CREATE TABLE hotel_managers (
    manager_id INT AUTO_INCREMENT PRIMARY KEY,
    hotel_id INT,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255) NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
);

show tables;
select * from customers;
select * from hotels;
select * from hotel_managers;
select * from customer_feedback;
select * from food_poisoning_cases;
select * from inspectors;
INSERT INTO inspectors (inspector_id, name, password) VALUES (1, 'inspector1', 'ipass1') ON DUPLICATE KEY UPDATE name='inspector1';
INSERT INTO inspectors (inspector_id, name, password) VALUES (2, 'inspector2', 'ipass2') ON DUPLICATE KEY UPDATE name='inspector2';
INSERT INTO inspectors (inspector_id, name, password) VALUES (3, 'inspector3', 'ipass3') ON DUPLICATE KEY UPDATE name='inspector3';
select * from inspections;
ALTER TABLE food_poisoning_cases
ADD COLUMN customer_id INT,
ADD FOREIGN KEY (customer_id) REFERENCES customers(id);
select * from food_poisoning_cases;