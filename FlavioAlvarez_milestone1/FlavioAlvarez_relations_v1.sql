CREATE TABLE business(
    business_id CHAR(22) Primary Key,
    name VARCHAR (50),
    address VARCHAR(50),
    city VARCHAR(20),
    state CHAR(2),
    postal_code CHAR(5),
    stars DECIMAL,
    review_count INT,
    ON UPDATE CASCADE,
    ON DELETE SET NULL
)

CREATE TABLE user (
    user_id CHAR(22) Primary Key,
    name VARCHAR(50) Primary Key,
    review_count INT,
    average_stars DECIMAL
    ON UPDATE CASCADE,
    ON DELETE SET NULL
)

CREATE TABLE review (
    review_id CHAR(22) Primary Key,
    user_id REFERENCES user(user_id),
    business_id REFERENCES business(business_id),
    text VARCHAR(1000),
    stars DECIMAL,
    date DATE
)

CREATE TABLE checkin (
    FOREIGN KEY (business_id) REFERENCES business(business_id),
    day VARCHAR(10),
    hour VARCHAR(5),
    number_checkins INT
)