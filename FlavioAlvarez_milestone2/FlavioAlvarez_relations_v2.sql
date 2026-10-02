CREATE TABLE Business(
    business_id CHAR(22) Primary Key,
    name VARCHAR (50),
    address VARCHAR(50),
    city VARCHAR(20),
    state CHAR(2),
    postal_code CHAR(5),
    stars DECIMAL,
    review_count INT,
    number_checkins INT,
    review_rating DECIMAL,
    ON UPDATE CASCADE,
    ON DELETE SET NULL
)

CREATE TABLE Review (
    review_id CHAR(22) Primary Key,
    business_id CHAR(22) REFERENCES business(business_id),
    review_text TEXT,
    stars INT,
    review_date DATE
)

CREATE TABLE Checkin (
    business_id CHAR (22) REFERENCES business(business_id),
    day VARCHAR(9),
    hour VARCHAR(5),
    number_checkins INT,
    Primary Key(business_id, day, hour)
)