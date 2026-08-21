-- -- total number of records

-- select count(*) as total_records
-- from online_retail;

-- -- preview the data

-- select *
-- from online_retail
-- limit 10;

-- -- number of unique invoices

-- select count(distinct invoice_no) as unique_invoices
-- from online_retail;

-- -- number of unique products

-- select count(distinct stock_code) as unique_products
-- from online_retail;

-- -- number of unique customers

-- select count(distinct customer_id) as unique_customers
-- from online_retail;

-- -- number of countries

-- select count(distinct country) as unique_countries
-- from online_retail;

-- -- transactions from the united kingdom

-- select *
-- from online_retail
-- where country = 'United Kingdom'
-- limit 10;

-- -- transactions with quantity greater than 10

-- select *
-- from online_retail
-- where quantity > 10
-- limit 10;

-- -- transactions with unit price greater than 5

-- select *
-- from online_retail
-- where unit_price > 5
-- limit 10;

-- -- uk transactions with quantity greater than 10 and unit price greater than 5

-- select
--     invoice_no,
--     description,
--     quantity,
--     unit_price,
--     country
-- from online_retail
-- where country = 'United Kingdom'
--   and quantity > 10
--   and unit_price > 5
-- limit 10;

-- -- most expensive transactions

-- select
--     invoice_no,
--     description,
--     quantity,
--     unit_price
-- from online_retail
-- order by unit_price desc
-- limit 10;

-- -- transactions with the highest quantity

-- select
--     invoice_no,
--     description,
--     quantity,
--     unit_price
-- from online_retail
-- order by quantity desc
-- limit 10;

-- -- cheapest transactions

-- select
--     invoice_no,
--     description,
--     quantity,
--     unit_price
-- from online_retail
-- order by unit_price asc
-- limit 10;

-- -- total quantity sold

-- select sum(quantity) as total_quantity
-- from online_retail;

-- -- average quantity per transaction

-- select avg(quantity) as average_quantity
-- from online_retail;

-- -- average unit price

-- select avg(unit_price) as average_unit_price
-- from online_retail;


-- -- minimum unit price

-- select min(unit_price) as minimum_unit_price
-- from online_retail;


-- -- maximum unit price

-- select max(unit_price) as maximum_unit_price
-- from online_retail;


-- -- number of transactions by country

-- select
--     country,
--     count(*) as transaction_count
-- from online_retail
-- group by country
-- order by transaction_count desc;


-- -- total quantity sold by country

-- select
--     country,
--     sum(quantity) as total_quantity
-- from online_retail
-- group by country
-- order by total_quantity desc;


-- -- average unit price by country

-- select
--     country,
--     avg(unit_price) as average_unit_price
-- from online_retail
-- group by country
-- order by average_unit_price desc;


-- -- number of unique customers by country

-- select
--     country,
--     count(distinct customer_id) as unique_customers
-- from online_retail
-- group by country
-- order by unique_customers desc;


-- -- revenue for each transaction

-- select
--     invoice_no,
--     stock_code,
--     description,
--     quantity,
--     unit_price,
--     quantity * unit_price as revenue
-- from online_retail
-- limit 10;


-- -- total revenue

-- select
--     sum(quantity * unit_price) as total_revenue
-- from online_retail;


-- -- revenue by country

-- select
--     country,
--     sum(quantity * unit_price) as total_revenue
-- from online_retail
-- group by country
-- order by total_revenue desc;


-- -- revenue by product

-- select
--     stock_code,
--     description,
--     sum(quantity * unit_price) as total_revenue
-- from online_retail
-- group by stock_code, description
-- order by total_revenue desc
-- limit 20;

-- -- revenue by customer

-- select
--     customer_id,
--     sum(quantity * unit_price) as total_spent
-- from online_retail
-- where customer_id is not null
-- group by customer_id
-- order by total_spent desc
-- limit 20;

-- -- number of invoices per customer

-- select
--     customer_id,
--     count(distinct invoice_no) as invoice_count
-- from online_retail
-- where customer_id is not null
-- group by customer_id
-- order by invoice_count desc
-- limit 20;

-- -- earliest and latest transaction

-- select
--     min(invoice_date) as first_transaction,
--     max(invoice_date) as last_transaction
-- from online_retail;

-- -- transactions by date

-- select
--     date(invoice_date) as transaction_date,
--     count(*) as transaction_count
-- from online_retail
-- group by date(invoice_date)
-- order by transaction_date;

-- -- revenue by date

-- select
--     date(invoice_date) as transaction_date,
--     sum(quantity * unit_price) as daily_revenue
-- from online_retail
-- group by date(invoice_date)
-- order by transaction_date;

-- -- countries with more than 1000 transactions

-- select
--     country,
--     count(*) as transaction_count
-- from online_retail
-- group by country
-- having count(*) > 1000
-- order by transaction_count desc;


-- -- products generating more than 10000 in revenue

-- select
--     stock_code,
--     description,
--     sum(quantity * unit_price) as total_revenue
-- from online_retail
-- group by stock_code, description
-- having sum(quantity * unit_price) > 10000
-- order by total_revenue desc;

-- -- categorize transactions based on quantity

-- select
--     invoice_no,
--     quantity,
--     case
--         when quantity >= 100 then 'High'
--         when quantity >= 10 then 'Medium'
--         else 'Low'
--     end as quantity_category
-- from online_retail
-- limit 20;

-- categorize products based on unit price

select
    stock_code,
    description,
    unit_price,
    case
        when unit_price >= 10 then 'Expensive'
        when unit_price >= 5 then 'Moderate'
        else 'Cheap'
    end as price_category
from online_retail
limit 10;