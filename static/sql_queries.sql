-- show databases
-- use world
-- show tables
-- show databases


-- EMPLOYEE DATA
-- use sales
-- select * from employee

-- TWITTER DATA 

-- CREATE TABLE
-- create table twitter_database ( 
-- 	id INT NOT NULL AUTO_INCREMENT,
--     tweet_id BIGINT,
-- 	user_name VARCHAR(255),
-- 	screen_name VARCHAR(255),
-- 	profile_url VARCHAR(65535),
-- 	created_at DATETIME,
-- 	created_at_date DATETIME,
-- 	created_at_day_name VARCHAR(10),
-- 	created_at_month VARCHAR(10),
-- 	created_at_year INT,
-- 	created_at_time1 varchar(50),
-- 	created_at_time2 varchar(50),
-- 	tweet_text TEXT,
-- 	location VARCHAR(255),
-- 	followers INT,
-- 	following INT,
-- 	listed_count INT,
-- 	profile_image VARCHAR(65535),
-- 	profile_banner_image VARCHAR(65535),
-- 	news_url_1 VARCHAR(65535),
-- 	news_url_2 VARCHAR(65535),
--     tweet_data_preprocessed TEXT,
--     sentiment INT,
--     PRIMARY KEY (id)
-- )

-- use twitter
-- show tables
-- show columns from tweet_data
-- select tweet_id from tweet_data
-- limit 10

-- show columns from twitter_database
select * from twitter_database		
-- select count(tweet_id) twitter_database

-- order by created_at desc
-- where created_at_date='2021-05-31 00:00:00'
-- 2021-06-01 05:27:39, 2021-06-01 00:00:00

-- select user_name from tweet_data
-- where location!='Indonesia'


-- MAKE SURE THE CONNECTION WITH LOCAL HOST IS DISCONNECTED WHEN MODIFYING DATABASE
-- DELETE COLUMN
-- alter table twitter_database
-- drop column created_at_day_name

-- INSERT COLUMN
-- alter table tweet_data
-- add column created_at_date DATETIME after created_at

-- INSERT COLUMN as first column and primary key
-- alter table twitter_database
-- add column id INT NOT NULL AUTO_INCREMENT PRIMARY KEY first

-- alter table twitter_database
-- add column created_at_day_name VARCHAR(10) after created_at_date

-- alter table twitter_database
-- add column sentiment_description VARCHAR(10) after sentiment

-- CHANGE DATA TYPE
-- alter table twitter_database
-- modify tweet_id BIGINT;

-- alter table twitter_database
-- modify tweet_data_preprocessed MEDIUMTEXT

-- alter table twitter_database
-- modify created_at_time2 varchar(50)

-- DELETE DATA with condition
-- delete from twitter_database
-- where sentiment_description is null