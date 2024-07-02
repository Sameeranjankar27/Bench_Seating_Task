CREATE DATABASE bench_sharing;
USE bench_sharing;
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
CREATE TABLE BenchTypes (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(255) NOT NULL
);

CREATE TABLE Resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    resource_name VARCHAR(255) NOT NULL,
    type_id INT,
    description TEXT,
    available_from DATE,
    company_id INT DEFAULT NULL,
    booked_at TIMESTAMP NULL,
    FOREIGN KEY (type_id) REFERENCES BenchTypes(type_id),
    FOREIGN KEY (company_id) REFERENCES Users(user_id)
);