-- 1. What was the total revenue to the nearest dollar for customers who have paid by credit card?
SELECT ROUND(SUM(revenue)) AS creadit_card_revenue
FROM customer_payment
WHERE cc_payments <> 0

-- 2. What percentage of customers who have purchased female items have paid by credit card?
SELECT COUNT(*) / (SELECT COUNT(*) FROM customer_payment)::float * 100 AS percentage
FROM customer_payment
WHERE cc_payments <> 0 AND female_items <> 0

-- 3. What was the average revenue for customers who used either iOS, Android or Desktop?
WITH _avg_revenue_ios_customer AS (
	SELECT 'ios' AS platform,ROUND(AVG(revenue)) AS avg_revenue
	FROM customer_payment
	WHERE ios_orders <> 0
), _avg_revenue_android_customer AS (
	SELECT 'android' AS platform, ROUND(AVG(revenue)) AS avg_revenue
	FROM customer_payment
	WHERE android_orders <> 0
), _avg_revenue_desktop_customer AS (
	SELECT 'desktop' AS platform, ROUND(AVG(revenue)) AS avg_revenue
	FROM customer_payment
	WHERE desktop_orders <> 0
)

SELECT *
FROM (SELECT * FROM _avg_revenue_ios_customer) AS ios
UNION (SELECT * FROM _avg_revenue_android_customer)
UNION (SELECT * FROM _avg_revenue_desktop_customer)

-- 4. We want to run an email campaign promoting a new mens luxury brand. Can you provide a list of customers we should send to?
SELECT customer_id
FROM customer_payment
WHERE male_items <> 0
