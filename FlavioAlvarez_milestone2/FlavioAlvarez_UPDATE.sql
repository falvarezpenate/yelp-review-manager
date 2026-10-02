-- Update number of checkins
UPDATE Business
SET number_checkins = (
    SELECT SUM(number_checkins)
    FROM Checkin
    WHERE Checkin.business_id = Business.business_id
)

-- Update review counts with actual values
UPDATE Business
SET review_count = (
    SELECT COUNT(*)
    FROM Review
    WHERE Review.business_id = Business.business_id
)


-- Update average ratings
UPDATE Business
SET review_rating = (
    SELECT AVG(stars)
    FROM Review
    WHERE Review.business_id = Business.business_id
)